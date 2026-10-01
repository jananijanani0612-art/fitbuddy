# FitBuddy Technical Architecture

```text
Browser
  │
  ├── HTML5 / CSS / JavaScript
  │       │
  │       └── fetch() → FastAPI REST API
  │
  ▼
FastAPI
  ├── /api/plans
  │     ├── Pydantic validation
  │     ├── Gemini plan generation
  │     ├── deterministic fallback
  │     └── SQLAlchemy persistence
  ├── /api/tips
  │     ├── Gemini tip generation
  │     └── fallback tip
  ├── /health
  └── /docs
        │
        ▼
SQLite (fitbuddy.db)

AI flow:
User input → prompt builder → Gemini → Pydantic JSON validation → DB
                         ↘ failure/no key → fallback → DB

Feedback:
Saved plan → feedback → prompt builder → Gemini/fallback → updated DB record
```

The AI provider is isolated in `app/ai/gemini.py`, so another LLM provider can be integrated later without changing the API/UI contract.
