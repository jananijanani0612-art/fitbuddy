import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..ai.gemini import generate_plan, generate_tip
from ..crud import create_plan_record, get_plan, list_plans, update_plan
from ..database import get_db
from ..schemas import FeedbackRequest, PlanCreate, PlanResponse, WorkoutPlan

router = APIRouter(prefix="/api/plans", tags=["Plans"])


def _response(record) -> PlanResponse:
    plan = WorkoutPlan.model_validate(json.loads(record.plan_json))
    return PlanResponse(
        id=record.id,
        name=record.name,
        goal=record.goal,
        intensity=record.intensity,
        experience=record.experience,
        equipment=record.equipment,
        plan=plan,
        tip=record.tip,
        source=record.source,
        created_at=record.created_at.isoformat(),
        updated_at=record.updated_at.isoformat(),
    )


@router.post("", response_model=PlanResponse)
def create_plan(payload: PlanCreate, db: Session = Depends(get_db)):
    plan, source = generate_plan(payload)
    tip, tip_source = generate_tip(payload.goal)
    final_source = "gemini" if source == "gemini" and tip_source == "gemini" else source
    record = create_plan_record(db, payload, plan, tip, final_source)
    return _response(record)


@router.get("", response_model=list[PlanResponse])
def get_plans(limit: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)):
    return [_response(item) for item in list_plans(db, limit)]


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan_by_id(plan_id: int, db: Session = Depends(get_db)):
    record = get_plan(db, plan_id)
    if not record:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _response(record)


@router.post("/{plan_id}/feedback", response_model=PlanResponse)
def regenerate_plan(plan_id: int, payload: FeedbackRequest, db: Session = Depends(get_db)):
    record = get_plan(db, plan_id)
    if not record:
        raise HTTPException(status_code=404, detail="Plan not found")

    class UserData:
        pass

    user = UserData()
    user.name = record.name
    user.age = record.age
    user.weight_kg = record.weight_kg
    user.goal = record.goal
    user.intensity = record.intensity
    user.experience = record.experience
    user.equipment = record.equipment

    plan, source = generate_plan(user, payload.feedback)
    tip, tip_source = generate_tip(record.goal)
    final_source = "gemini" if source == "gemini" and tip_source == "gemini" else source
    updated = update_plan(db, record, plan, tip, payload.feedback, final_source)
    return _response(updated)
