import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Plan
from .schemas import PlanCreate


def create_plan_record(db: Session, user: PlanCreate, plan: dict, tip: str, source: str) -> Plan:
    record = Plan(
        name=user.name,
        age=user.age,
        weight_kg=user.weight_kg,
        goal=user.goal,
        intensity=user.intensity,
        experience=user.experience,
        equipment=user.equipment,
        plan_json=json.dumps(plan),
        tip=tip,
        source=source,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_plan(db: Session, plan_id: int) -> Plan | None:
    return db.get(Plan, plan_id)


def list_plans(db: Session, limit: int = 20) -> list[Plan]:
    return list(db.scalars(select(Plan).order_by(Plan.created_at.desc()).limit(limit)))


def update_plan(db: Session, record: Plan, plan: dict, tip: str, feedback: str, source: str) -> Plan:
    record.plan_json = json.dumps(plan)
    record.tip = tip
    record.feedback = feedback
    record.source = source
    record.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(record)
    return record
