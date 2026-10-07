# Agent Instructions: Quest Me

These instructions guide the implementation of Quest Me, an AI-powered outdoor adventure PWA.

## Core Philosophy
"The AI generates the adventure. The human lives it." 
The screen is the shortest part of the experience.

## Development Workflow
Work in vertical slices. Prioritize the end-to-end loop:
`Generate Quest` → `Start Quest` → `Phone Down/Go Outside` → `Photo Evidence` → `Vision Verification` → `Completion/XP`.

## Technical Constraints
- **Frontend**: React, Vite, TypeScript, PWA, Mobile-First.
- **Backend**: Python, FastAPI, Pydantic, SQLite.
- **AI**: Ollama (Local/Open-weight). Structured JSON output is mandatory.
- **Verification**: Use open-weight vision models for photo evidence.
- **Deployment**: Render.

## Engineering Principles
- **Do NOT overengineer**: No complex auth, no vector DBs, no microservices for MVP.
- **Safety First**: Quests must be safe and physically possible.
- **UI Quality**: "Field notebook + outdoor adventure + playful AI". Avoid "Enterprise SaaS" look.
- **Vertical Slices**: Implement, Run, Test, Inspect, Fix, Commit.
