def _exercise(name, sets, reps, rest=60, notes="Use controlled form."):
    return {
        "name": name,
        "sets": sets,
        "reps": reps,
        "rest_seconds": rest,
        "notes": notes,
    }


def generate_fallback_plan(user, feedback: str | None = None) -> dict:
    sets = {"low": 2, "medium": 3, "high": 4}[user.intensity]
    cardio_name, cardio_reps = {
        "weight loss": ("Brisk walk / cycling", "20-35 min"),
        "muscle gain": ("Easy incline walk", "15-25 min"),
        "general wellness": ("Brisk walk", "20-30 min"),
    }[user.goal]

    strength = [
        _exercise("Squat", sets, "8-12"),
        _exercise("Push-up", sets, "6-12", notes="Use an elevated surface if needed."),
        _exercise("Hip hinge / Romanian deadlift pattern", sets, "8-12"),
        _exercise("Row", sets, "8-12"),
    ]
    core = [
        _exercise("Dead bug", 2, "8-12 / side", 45),
        _exercise("Plank", 2, "20-45 sec", 45),
    ]

    if user.goal == "muscle gain":
        days = [
            ("Day 1", "Full-body strength", strength),
            ("Day 2", "Active recovery", [_exercise(cardio_name, 1, cardio_reps, 30)]),
            ("Day 3", "Strength + core", strength[:3] + core),
            ("Day 4", "Rest and mobility", []),
            ("Day 5", "Full-body strength", strength),
            ("Day 6", "Light cardio", [_exercise(cardio_name, 1, cardio_reps, 30)]),
            ("Day 7", "Rest and mobility", []),
        ]
    elif user.goal == "weight loss":
        days = [
            ("Day 1", "Full-body + cardio", strength + [_exercise(cardio_name, 1, "15-25 min", 30)]),
            ("Day 2", "Cardio + core", [_exercise(cardio_name, 1, cardio_reps, 30)] + core),
            ("Day 3", "Full-body strength", strength),
            ("Day 4", "Recovery walk", [_exercise("Easy walk", 1, "20-30 min", 30)]),
            ("Day 5", "Full-body + cardio", strength + [_exercise(cardio_name, 1, "15-25 min", 30)]),
            ("Day 6", "Mobility + easy cardio", [_exercise("Mobility flow", 2, "5-8 min", 30), _exercise(cardio_name, 1, "15-25 min", 30)]),
            ("Day 7", "Rest", []),
        ]
    else:
        days = [
            ("Day 1", "Full-body strength", strength),
            ("Day 2", "Cardio", [_exercise(cardio_name, 1, cardio_reps, 30)]),
            ("Day 3", "Strength + core", strength[:3] + core),
            ("Day 4", "Recovery", [_exercise("Mobility flow", 2, "5-8 min", 30)]),
            ("Day 5", "Full-body strength", strength),
            ("Day 6", "Cardio + core", [_exercise(cardio_name, 1, cardio_reps, 30)] + core),
            ("Day 7", "Rest", []),
        ]

    feedback_lower = (feedback or "").lower()
    if "rest" in feedback_lower:
        days[5] = ("Day 6", "Extra recovery", [])
    if "cardio" in feedback_lower:
        days[0][2].append(_exercise(cardio_name, 1, "15-25 min", 30))

    result_days = []
    for day, focus, exercises in days:
        duration = 20 if not exercises else min(75, 10 + len(exercises) * 8)
        result_days.append({
            "day": day,
            "focus": focus,
            "duration_minutes": duration,
            "exercises": exercises,
            "recovery": (
                "Finish with gentle mobility and prioritize hydration and sleep."
                if exercises
                else "Take a comfortable rest day; light movement is optional."
            ),
        })

    return {
        "title": f"7-Day {user.goal.title()} Plan",
        "summary": f"A {user.intensity}-intensity plan designed for a {user.experience} level.",
        "safety_note": "Warm up before training, use controlled form, and stop if you experience pain, dizziness, or unusual symptoms.",
        "days": result_days,
    }


def fallback_tip(goal: str) -> str:
    return {
        "weight loss": "Build meals around protein, vegetables, whole grains, and minimally processed foods; pair this with consistent sleep and hydration.",
        "muscle gain": "Include a protein-rich meal or snack around training and eat enough overall to support recovery and gradual muscle growth.",
        "general wellness": "Aim for balanced meals, regular hydration, consistent sleep, and a sustainable mix of strength, cardio, and mobility work.",
    }.get(goal, "Prioritize balanced nutrition, hydration, sleep, and gradual progress.")
