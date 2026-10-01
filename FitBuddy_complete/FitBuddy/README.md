# FitBuddy — AI-Powered Fitness Planner

FitBuddy is a full-stack FastAPI application that creates personalized 7-day workout plans and nutrition/recovery tips from a user's age, weight, goal, experience, intensity, and available equipment.

## Features

- FastAPI REST API
- SQLite persistence with SQLAlchemy
- Google Gemini integration using the official `google-genai` SDK
- Automatic local fallback generation when Gemini is unavailable
- 7-day workout plans
- Feedback-based plan regeneration
- Nutrition/recovery tips
- Responsive HTML/CSS/JavaScript interface
- Pydantic validation
- Swagger/OpenAPI docs
- Pytest tests
- VS Code launch/tasks configuration

## Health and safety

FitBuddy provides general wellness guidance. It is not a medical device and does not replace a doctor, registered dietitian, physiotherapist, or qualified trainer. Users with medical conditions, injuries, pregnancy, eating-disorder history, or other health concerns should obtain appropriate professional advice before exercising or changing diet.

## Requirements

- Python 3.10 or newer recommended
- VS Code
- Git
- Internet connection for Gemini
- Gemini API key is optional for local testing because the app has a fallback generator

## Setup in VS Code

### Windows PowerShell

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and optionally set:

```env
GEMINI_API_KEY=your_gemini_api_key
```

If the key is empty, the app uses the built-in fallback planner.

## Run

```bash
python run.py
```

Or:

```bash
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

SQLite database `fitbuddy.db` is created automatically.

## Test

```bash
pytest -q
```

## API

### POST `/api/plans`

```json
{
  "name": "Janani",
  "age": 24,
  "weight_kg": 62,
  "goal": "muscle gain",
  "intensity": "medium",
  "experience": "beginner",
  "equipment": "home"
}
```

### GET `/api/plans`

Returns recent saved plans.

### GET `/api/plans/{id}`

Returns one saved plan.

### POST `/api/plans/{id}/feedback`

```json
{
  "feedback": "Please add more cardio and one extra rest day."
}
```

### GET `/api/tips?goal=muscle%20gain`

Returns a nutrition/recovery tip.

### GET `/health`

Returns service health.

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   ├── gemini.py
│   │   └── fallback.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── plans.py
│   │   └── tips.py
│   ├── templates/index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── tests/test_api.py
├── .vscode/
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
├── ARCHITECTURE.md
└── README.md
```

## VS Code

1. Extract the ZIP.
2. Open the `FitBuddy` folder in VS Code.
3. Select the `.venv` Python interpreter.
4. Install dependencies from the terminal.
5. Copy `.env.example` to `.env`.
6. Optionally add the Gemini API key.
7. Press `F5` and choose `FitBuddy FastAPI`, or run `python run.py`.
8. Open `http://127.0.0.1:8000`.

The first request without a Gemini key is intentionally handled locally so the project can be demonstrated without external AI credentials.

## Production considerations

For production, add authentication/authorization, rate limiting, secure secret management, structured logging, monitoring, a managed database such as PostgreSQL, restrictive CORS, and an appropriate privacy/security design for any health-related information.
