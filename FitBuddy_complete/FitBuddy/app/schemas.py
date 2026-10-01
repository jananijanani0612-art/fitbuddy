from typing import Literal

from pydantic import BaseModel, Field, field_validator


Goal = Literal["weight loss", "muscle gain", "general wellness"]
Intensity = Literal["low", "medium", "high"]
Experience = Literal["beginner", "intermediate", "advanced"]
Equipment = Literal["home", "gym", "bodyweight"]


class PlanCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=13, le=100)
    weight_kg: float = Field(gt=20, le=400)
    goal: Goal
    intensity: Intensity
    experience: Experience = "beginner"
    equipment: Equipment = "home"

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = " ".join(value.strip().split())
        if len(value) < 2:
            raise ValueError("Name must contain at least two characters.")
        return value


class FeedbackRequest(BaseModel):
    feedback: str = Field(min_length=3, max_length=1000)


class Exercise(BaseModel):
    name: str
    sets: int = Field(ge=1, le=10)
    reps: str
    rest_seconds: int = Field(ge=15, le=300)
    notes: str = ""


class DayPlan(BaseModel):
    day: str
    focus: str
    duration_minutes: int = Field(ge=10, le=180)
    exercises: list[Exercise]
    recovery: str


class WorkoutPlan(BaseModel):
    title: str
    summary: str
    safety_note: str
    days: list[DayPlan] = Field(min_length=7, max_length=7)


class PlanResponse(BaseModel):
    id: int
    name: str
    goal: str
    intensity: str
    experience: str
    equipment: str
    plan: WorkoutPlan
    tip: str
    source: str
    created_at: str
    updated_at: str


class TipResponse(BaseModel):
    goal: str
    tip: str
