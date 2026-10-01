import json
import logging

from pydantic import ValidationError

from ..config import get_settings
from ..schemas import WorkoutPlan
from .fallback import fallback_tip, generate_fallback_plan
from .prompts import build_plan_prompt, build_tip_prompt

logger = logging.getLogger(__name__)


def _client():
    settings = get_settings()
    if not settings.gemini_api_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=settings.gemini_api_key)
    except Exception:
        logger.exception("Could not initialize Gemini client.")
        return None


def generate_plan(user, feedback: str | None = None) -> tuple[dict, str]:
    client = _client()
    if client is None:
        return generate_fallback_plan(user, feedback), "fallback"

    settings = get_settings()
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=build_plan_prompt(user, feedback),
            config={
                "response_mime_type": "application/json",
                "temperature": 0.4,
            },
        )
        data = json.loads(response.text)
        validated = WorkoutPlan.model_validate(data)
        return validated.model_dump(), "gemini"
    except (json.JSONDecodeError, ValidationError, Exception):
        logger.exception("Gemini plan generation failed; using fallback.")
        return generate_fallback_plan(user, feedback), "fallback"


def generate_tip(goal: str) -> tuple[str, str]:
    client = _client()
    if client is None:
        return fallback_tip(goal), "fallback"

    settings = get_settings()
    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=build_tip_prompt(goal),
            config={"temperature": 0.4},
        )
        tip = response.text.strip()
        if not tip:
            raise ValueError("Empty Gemini response")
        return tip[:1000], "gemini"
    except Exception:
        logger.exception("Gemini tip generation failed; using fallback.")
        return fallback_tip(goal), "fallback"
