from fastapi import APIRouter, HTTPException, Query

from ..ai.gemini import generate_tip
from ..schemas import TipResponse

router = APIRouter(prefix="/api/tips", tags=["Tips"])
VALID_GOALS = {"weight loss", "muscle gain", "general wellness"}


@router.get("", response_model=TipResponse)
def get_tip(goal: str = Query(...)):
    if goal not in VALID_GOALS:
        raise HTTPException(status_code=422, detail="Unsupported fitness goal")
    tip, _ = generate_tip(goal)
    return TipResponse(goal=goal, tip=tip)
