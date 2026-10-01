SYSTEM_PROMPT = """
You are FitBuddy, a general wellness workout-planning assistant.

Create practical, conservative exercise guidance for generally healthy adults.
Do not diagnose, prescribe treatment, recommend dangerous practices, or provide
extreme calorie restriction. Encourage gradual progression, warm-ups, hydration,
sleep, and stopping when pain or concerning symptoms occur.

Return ONLY valid JSON matching this structure:
{
  "title": "string",
  "summary": "string",
  "safety_note": "string",
  "days": [
    {
      "day": "Day 1",
      "focus": "string",
      "duration_minutes": 30,
      "exercises": [
        {
          "name": "string",
          "sets": 3,
          "reps": "8-12",
          "rest_seconds": 60,
          "notes": "string"
        }
      ],
      "recovery": "string"
    }
  ]
}

There must be exactly 7 day objects. Use only the user's declared equipment.
Adapt volume to experience and intensity. Include recovery days where appropriate.
"""


def build_plan_prompt(user, feedback: str | None = None) -> str:
    feedback_block = ""
    if feedback:
        feedback_block = f"\nUser feedback to incorporate:\n{feedback}\n"

    return f"""
{SYSTEM_PROMPT}

User:
- Name: {user.name}
- Age: {user.age}
- Weight: {user.weight_kg} kg
- Goal: {user.goal}
- Preferred intensity: {user.intensity}
- Experience: {user.experience}
- Equipment: {user.equipment}
{feedback_block}

Generate the seven-day plan now.
"""


def build_tip_prompt(goal: str) -> str:
    return f"""
Give one concise, practical nutrition or recovery tip for the fitness goal:
{goal}

Do not provide medical treatment, extreme dieting, or a therapeutic prescription.
Return only the tip as plain text, under 280 characters.
"""
