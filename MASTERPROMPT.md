# QUEST ME — MASTER DEVELOPMENT PROMPT

You are the primary engineering agent for this project.

We are building **Quest Me**, a new project for the **Hacktoberfest 2026 DEV Challenge Week 1: “Touch Grass”**.

The project must be genuinely useful, technically credible, visually polished, and demonstrably built during the challenge window.

## 0. THE PRODUCT

### Core idea

Build a mobile-first PWA called:

# Quest Me

Tagline:

> **Touch Grass. Literally.**

The core philosophy is:

> **The AI generates the adventure. The human lives it.**

Quest Me uses open-weight/local AI to generate short real-world outdoor quests.

The user:

1. Opens Quest Me.
2. Starts a quest.
3. The AI generates a structured outdoor challenge.
4. The app tells them to put the phone down.
5. They go outside.
6. They complete the objectives.
7. They return and submit photo evidence.
8. A local/open-weight vision model checks the evidence.
9. The quest is completed.
10. The user earns XP and progresses.

The screen should be the **shortest part of the experience**.

This is not supposed to become another AI chat application.

---

# 1. NON-NEGOTIABLE GOALS

The MVP must demonstrate this complete vertical slice:

```text
Generate Quest
      ↓
Start Quest
      ↓
Phone Down
      ↓
Go Outside
      ↓
Take Evidence Photo
      ↓
Vision Verification
      ↓
Quest Completed
      ↓
XP / Progress
```

If time becomes limited, prioritize this loop above everything else.

Do NOT spend the majority of development time on:

* authentication
* social feeds
* leaderboards
* complex profiles
* elaborate databases
* vector databases
* unnecessary microservices
* complicated agent frameworks
* overengineered deployment
* fancy AI research infrastructure

The goal is a **great working demo**, not a startup-scale backend.

---

# 2. HACKTOBERFEST CONTEXT

This project is being built specifically for the Hacktoberfest 2026 DEV Challenge Week 1 theme:

**Touch Grass**

The project should therefore make the connection to the theme obvious.

The final product should encourage:

* going outdoors
* observing the physical world
* reducing passive screen time
* interacting with surroundings
* completing small real-world challenges

Do not make this merely a metaphorical "touch grass" app.

The user should literally have to leave the screen and do something outside.

---

# 3. OPEN-WEIGHT AI IS CENTRAL

Open-weight/local AI is not just a checkbox.

It should be part of the actual product architecture.

Core product AI should preferably run through:

```text
FastAPI
   ↓
Ollama
   ↓
Open-weight model
```

The architecture must make model selection configurable.

Do NOT hard-code the entire product around one specific model.

Inspect the available environment and installed Ollama models before choosing models.

Prefer models that can realistically run on the available local hardware.

---

# 4. TWO DIFFERENT AI LAYERS

Keep these concepts separate.

## Development AI

Claude Code is the **engineering agent/harness**.

Development environment:

```text
Claude Code
    ↓
Ollama / configured local model
    ↓
Developer environment
```

DevRelay is being used to capture the agent-development workflow.

## Product AI

Quest Me itself has AI agents/services:

### Quest Agent

Responsible for generating quests.

### Vision Agent

Responsible for checking submitted photo evidence.

These are product features and should be implemented as application components.

Do not confuse the development agent with the product agents.

---

# 5. CLAUDE CODE SKILLS

Before implementing anything:

1. Inspect the available Claude Code skills.
2. Identify skills relevant to this project.
3. Use relevant skills where they materially improve implementation.
4. Do NOT blindly invoke every available skill.

Look particularly for skills related to:

* React
* TypeScript
* Vite
* PWA
* UI/UX
* mobile design
* accessibility
* FastAPI
* Python
* testing
* browser testing
* debugging
* security
* API design
* structured outputs
* agents/tools
* documentation
* Git/GitHub
* vision/image processing

If a skill gives you a better established workflow, use it.

Do not waste time invoking irrelevant skills merely to say they were used.

---

# 6. TECH STACK

Use:

## Frontend

* React
* Vite
* TypeScript
* mobile-first responsive design
* PWA support
* browser camera APIs where practical

## Backend

* Python
* FastAPI
* Pydantic

## Database

* SQLite for MVP

Keep the database simple.

Potential tables:

```text
users
quests
quest_objectives
evidence
progress
```

Authentication is NOT required for the first MVP unless there is a compelling reason.

A local/demo user is acceptable.

## AI

* Ollama
* open-weight models
* configurable model names
* structured JSON output

## Deployment

Use Render where practical.

Frontend and backend should be deployable independently if necessary.

---

# 7. PARTNER TECHNOLOGY STRATEGY

We should use partner technology only when it improves the actual product.

Do not bolt technologies on just to enter prize categories.

## Render — USE

Use Render for deployment/demo hosting.

This should be a genuine part of the deployment story.

Potential structure:

```text
React/Vite PWA
      ↓
Render
      ↓
FastAPI
```

The local Ollama setup remains the primary development/product AI environment.

If Render cannot practically host local Ollama inference, do NOT fake it.

Create a clean abstraction so inference providers can be switched.

Document the deployment limitation honestly.

---

# 8. ELEVENLABS — STRONGLY CONSIDER FOR MVP

Use ElevenLabs if it can be integrated quickly and meaningfully.

The strongest use case is:

## Voice-guided outdoor quests

After the quest begins, instead of requiring the user to keep staring at the phone:

```text
"Your quest starts now."

"Find a plant you have never noticed before."

"Look for a naturally repeating pattern."

"Bonus: find something yellow that isn't manufactured."

"Now put your phone away."
```

Voice should reinforce the project's central philosophy:

> The screen should get out of the way.

Do NOT make ElevenLabs the core AI.

Quest generation and verification should remain based on open/local AI.

ElevenLabs is an enhancement for the outdoor experience.

If integration becomes a time sink, skip it and finish the core loop.

---

# 9. BACKBOARD — OPTIONAL

Backboard can be considered for persistent memory/personalization.

Potential future use:

```text
Completed quests
     ↓
Quest history
     ↓
Preference summary
     ↓
Future quest generation
```

However:

DO NOT upload sensitive raw information unnecessarily.

Especially avoid sending:

* raw location history
* raw photos
* unnecessary personal information

If Backboard is implemented, use it only for useful preference/context memory.

For example:

```json
{
  "preferred_duration": "20-30 minutes",
  "recent_themes": ["nature", "observation"],
  "difficulty": "medium",
  "completed_count": 8
}
```

Backboard is optional.

Do not allow it to delay the MVP.

---

# 10. TINKER — OPTIONAL / RESEARCH TRACK

Tinker is interesting because this challenge focuses on open-weight models.

However, Tinker must NOT become an MVP dependency unless the implementation is genuinely quick.

Possible future/research use:

* fine-tune a small quest-generation model
* experiment with LoRA
* compare base vs adapted quest generation
* document the experiment
* potentially use the trained weights later

This is a bonus.

The MVP must work without Tinker.

Do not spend the final days of the challenge trying to train a model when the actual product is incomplete.

---

# 11. QUEST GENERATION

Quest generation must return structured data.

Do NOT rely on arbitrary prose from the LLM.

Use a schema similar to:

```json
{
  "title": "Urban Naturalist",
  "description": "A short observation quest...",
  "duration_minutes": 20,
  "difficulty": "easy",
  "objectives": [
    {
      "id": "objective_1",
      "description": "Find a plant you have never noticed before.",
      "evidence_required": true
    },
    {
      "id": "objective_2",
      "description": "Find a naturally repeating pattern.",
      "evidence_required": true
    },
    {
      "id": "objective_3",
      "description": "Find something in nature changed by humans.",
      "evidence_required": true
    }
  ],
  "bonus": "Find something yellow that isn't manufactured.",
  "xp": 100
}
```

Use Pydantic to validate the result.

The frontend should never blindly trust raw LLM output.

---

# 12. QUEST QUALITY

Generated quests must be:

* physically possible
* safe
* understandable
* short
* interesting
* location-flexible
* achievable without special equipment
* suitable for ordinary outdoor environments

Avoid quests requiring:

* trespassing
* dangerous roads
* climbing
* entering unsafe areas
* interacting with strangers
* handling animals
* dangerous plants
* dangerous objects
* specialized equipment

The model should generate adventures, not liabilities.

---

# 13. QUEST TYPES

Start with several categories.

Examples:

### Urban Naturalist

Observe nature in an urban environment.

### Pattern Hunter

Find repeating shapes/patterns.

### Tiny Explorer

Find three small details most people would miss.

### Human + Nature

Find places where humans have altered natural elements.

### Color Hunt

Find naturally occurring colors.

### Five-Minute Scientist

Make simple observations and hypotheses.

### Shadow Quest

Explore shadows and changing shapes.

The generator can combine themes.

---

# 14. QUEST STATE MACHINE

Implement explicit quest states.

```text
GENERATED
    ↓
STARTED
    ↓
IN_PROGRESS
    ↓
EVIDENCE_SUBMITTED
    ↓
VERIFIED
    ↓
COMPLETED
```

Objectives should have their own state:

```text
PENDING
    ↓
EVIDENCE_SUBMITTED
    ↓
VERIFIED
```

or:

```text
REJECTED
```

Do not build complicated workflow infrastructure.

Simple enums and database fields are enough.

---

# 15. VISION VERIFICATION

The vision model should evaluate whether a submitted photo provides reasonable evidence for the objective.

Example:

Objective:

> Find a plant you have never noticed before.

Photo submitted.

Vision model returns:

```json
{
  "valid": true,
  "confidence": 0.87,
  "reason": "The image clearly contains a living plant."
}
```

Important:

Do not represent model confidence as scientifically calibrated probability.

Use it only as an internal/model confidence indicator.

The UI should use simple language such as:

> Evidence accepted.

or:

> Hmm, I can't verify that one. Try another photo.

The vision model should not need to perfectly understand the user's intent.

It only needs to provide a reasonable evidence check.

---

# 16. PHOTO PRIVACY

Photos are potentially sensitive.

Design the architecture so that:

* photos do not need permanent storage unless required
* temporary evidence can be deleted after verification
* local inference is preferred
* privacy is clearly explained
* unnecessary metadata is avoided

Do not build a giant image storage system.

For MVP, temporary processing is enough.

---

# 17. LOCATION

Location can improve quests but must NOT be required.

Do not make location permission mandatory.

If location is available, use coarse contextual information such as:

```text
urban
suburban
park-like
campus
```

rather than unnecessarily storing precise location history.

Potential future tool:

```text
get_location_context()
```

The agent can then adapt quests.

Example:

```text
campus → campus-friendly quest

park → nature-heavy quest

urban → street-observation quest
```

But the app must still work without location.

---

# 18. WEATHER

Weather is another optional context input.

Potential tool:

```text
get_weather()
```

This can influence quest generation.

Examples:

Rain:

```text
Covered/short quest
```

Cool evening:

```text
Longer walking quest
```

Hot weather:

```text
Short shaded quest
```

Do not build a giant weather subsystem.

A small abstraction is enough.

---

# 19. AGENT TOOL DESIGN

Use tools where the agent genuinely benefits from them.

Potential tools:

```text
get_time()
get_weather()
get_location_context()
get_recent_quests()
get_user_preferences()
```

But deterministic application operations should remain normal code.

For example:

DO NOT ask an LLM to calculate XP.

Normal code should do:

```text
quest_completed
    ↓
+100 XP
    ↓
update database
```

The agent generates/adapts content.

The application controls truth/state.

---

# 20. LIGHTWEIGHT MEMORY

No vector database is required.

Use SQLite.

Store useful history such as:

```text
completed quests
quest categories
difficulty
objectives completed
objectives rejected
recent themes
XP
streak
```

This gives enough personalization for MVP.

Example:

If the user completed five nature quests recently, the next generation request can say:

> Avoid repeating recent themes.

---

# 21. UI / UX

The visual design should feel like:

* outdoor adventure
* field research
* exploration
* playful AI
* modern mobile app

NOT:

* enterprise SaaS
* generic dashboard
* generic ChatGPT clone
* boring Bootstrap form

The UI should feel like an invitation to go outside.

---

# 22. HOME SCREEN

Design around:

```text
QUEST ME

Touch Grass.
Literally.

[  Start a Quest  ]

12
Quests Completed

340 XP
Current Progress

🔥 4 day streak
```

Keep it visually strong and simple.

---

# 23. QUEST SCREEN

Show:

```text
URBAN NATURALIST

20 MIN
EASY

Explore your surroundings
with fresh eyes.

□ Find a plant you've never noticed
□ Find a repeating natural pattern
□ Find something in nature changed by humans

BONUS
Find something yellow that isn't manufactured.

[ START QUEST ]
```

Once started:

```text
PHONE DOWN.

Go explore.

We'll be here when you get back.
```

This screen is important.

It communicates the entire philosophy of the product.

---

# 24. EVIDENCE SCREEN

When the user returns:

```text
OBJECTIVE 1

Find a plant you've never noticed before.

[ TAKE PHOTO ]

or

[ CHOOSE PHOTO ]
```

Use the browser camera when available.

Mobile UX is the priority.

---

# 25. VERIFICATION UI

After submitting:

```text
Checking your evidence...

✓ Evidence accepted

Nice find.

+25 XP
```

For rejection:

```text
Hmm...

I couldn't verify this one.

Try getting closer or finding a clearer example.

[ TRY AGAIN ]
```

Keep it friendly.

---

# 26. COMPLETION SCREEN

Example:

```text
QUEST COMPLETE

Urban Naturalist

3 / 3 objectives
+100 XP

🔥 Streak: 5 days

You actually went outside.

[ NEW QUEST ]
```

The wording can be playful.

---

# 27. PWA

The app must behave well on mobile.

Implement:

* responsive layout
* installable PWA
* manifest
* icons
* sensible viewport
* mobile navigation
* camera access
* offline-friendly shell where practical

Do NOT promise fully offline AI inference unless we actually implement it.

A future goal can be:

> Eventually run both quest generation and vision locally on-device.

For MVP, local inference can mean local backend/Ollama during development.

Be technically honest.

---

# 28. RESPONSIVE DESIGN

Desktop should still work for development/demo purposes.

But mobile is the primary target.

Test at least:

```text
360px
390px
430px
768px
desktop
```

Avoid layouts that look like desktop websites squeezed onto phones.

---

# 29. ACCESSIBILITY

Implement basic accessibility from the beginning.

Use:

* semantic HTML
* labels
* keyboard support
* sufficient contrast
* visible focus states
* meaningful buttons
* alt text
* accessible loading/error states

Do not sacrifice usability for visual effects.

---

# 30. ERROR HANDLING

The application must survive:

* Ollama unavailable
* model unavailable
* malformed LLM JSON
* vision model failure
* camera permission denied
* location denied
* weather unavailable
* network errors
* empty model response
* invalid evidence

The UI should show useful recovery paths.

Example:

```text
Quest generation is taking a little longer.

[ Try Again ]
```

Do not expose raw stack traces to users.

---

# 31. DEVELOPMENT WORKFLOW

Work in vertical slices.

Recommended order:

## Phase 1 — Skeleton

Create:

```text
frontend/
backend/
README.md
.env.example
.gitignore
```

Get frontend and backend running.

---

## Phase 2 — Static UX

Build:

* home
* quest screen
* start state
* evidence screen
* completion screen

Use mocked quest data initially.

Make the experience feel good before wiring AI.

---

## Phase 3 — Quest Agent

Connect:

```text
FastAPI
  ↓
Ollama
  ↓
structured quest
```

Add Pydantic validation.

---

## Phase 4 — Persistence

Add SQLite.

Implement:

* quests
* objectives
* evidence metadata
* XP
* completion
* history

---

## Phase 5 — Vision Agent

Implement photo submission.

Connect image to local/open-weight vision model.

Return structured verification.

---

## Phase 6 — Real End-to-End Loop

Verify:

```text
Generate
→ Start
→ Go outside
→ Photo
→ Vision
→ Complete
→ XP
```

This is the critical milestone.

---

## Phase 7 — PWA + Polish

Add:

* installability
* mobile polish
* loading states
* error states
* transitions
* accessibility

---

## Phase 8 — ElevenLabs

If the core loop is stable:

Add voice guidance.

Keep it optional.

---

## Phase 9 — Render

Deploy a demo.

Document architecture and deployment.

---

## Phase 10 — Optional Partner Experiments

Only after the MVP works:

* Backboard memory
* Tinker experiment
* additional integrations

---

# 32. TESTING

Create useful tests.

Backend:

* Pydantic schema validation
* quest generation parsing
* invalid LLM response handling
* quest state transitions
* XP calculation
* objective verification handling

Frontend:

* main quest flow
* loading/error states
* camera permission fallback
* completion state

Do not chase arbitrary 100% coverage.

Test the important paths.

---

# 33. SECURITY

Do not commit secrets.

Create:

```text
.env.example
```

Never commit:

```text
.env
API keys
tokens
credentials
private URLs
```

Validate uploaded files.

Limit acceptable image size/type.

Do not blindly trust model output.

Do not expose internal errors.

---

# 34. PROJECT STRUCTURE

Use a clean structure.

A reasonable starting point:

```text
quest-me/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── agents/
│   │   ├── tools/
│   │   └── main.py
│   └── tests/
│
├── docs/
│
├── .env.example
├── .gitignore
└── README.md
```

You may improve this structure if there is a clear reason.

Do not create dozens of files prematurely.

---

# 35. API DESIGN

Keep the API simple.

Possible endpoints:

```text
GET  /health

POST /api/quests/generate

POST /api/quests/{quest_id}/start

GET  /api/quests/{quest_id}

POST /api/quests/{quest_id}/objectives/{objective_id}/evidence

POST /api/quests/{quest_id}/complete

GET  /api/progress
```

Use Pydantic request/response models.

Do not return arbitrary internal objects.

---

# 36. CONFIGURATION

Make model configuration environment-driven.

For example:

```env
OLLAMA_BASE_URL=http://localhost:11434
QUEST_MODEL=...
VISION_MODEL=...
```

Do not assume the model name before inspecting the environment.

The application should make it easy to swap models.

---

# 37. LOCAL DEVELOPMENT

Before making architecture decisions, inspect:

* available Python version
* Node version
* npm/pnpm/bun availability
* Ollama installation
* available Ollama models
* available hardware
* Git state
* repository state

Do not assume anything that can be checked.

Use the tools available in the environment.

---

# 38. GIT DISCIPLINE

Commit working milestones.

Suggested commits:

```text
chore: initialize Quest Me
feat: add mobile quest experience
feat: add quest generation agent
feat: add quest persistence
feat: add vision evidence verification
feat: add XP and quest completion
feat: add PWA support
feat: add voice guidance
chore: deploy demo
docs: add project documentation
```

Do not make one giant commit at the end.

---

# 39. README

The README is extremely important.

It should explain:

## Quest Me

One-line description.

## Why?

Explain the problem:

People increasingly use screens for everything.

Quest Me uses AI to create a reason to stop looking at the screen.

## Demo

Add demo link once deployed.

## Screenshots

Add polished screenshots.

## Architecture

Show:

```text
User
 ↓
PWA
 ↓
FastAPI
 ↓
Quest Agent / Vision Agent
 ↓
Ollama
 ↓
Open-weight models
```

## Open Innovation

Explain:

* local inference
* open-weight models
* model portability
* inspectability
* privacy
* customization
* future offline potential

## Partner Technologies

Clearly state actual usage:

* Render
* ElevenLabs if implemented
* Backboard if implemented
* Tinker if implemented

Do not claim technologies that were not used.

## Local Setup

Give exact commands.

## Environment Variables

Explain `.env.example`.

## Architecture Decisions

Explain why:

* FastAPI
* SQLite
* Ollama
* local/open-weight AI
* PWA

were chosen.

---

# 40. DEMO VIDEO

The final demo should be short and visual.

Prefer vertical/mobile framing where possible.

Suggested sequence:

```text
0:00
Open Quest Me

0:05
Generate quest

0:10
Quest appears

0:15
"PHONE DOWN."

0:18
User goes outside

0:25
User finds objective

0:30
Take photo

0:35
AI verifies

0:40
Quest complete

0:45
XP/streak

0:50
Phone goes away again
```

The demo should make the product understandable without narration.

---

# 41. DEV.TO ARTICLE

The final submission should be written as a strong technical/product story.

Structure:

## What I Built

Explain Quest Me.

## Demo

Link/video.

## How I Built It

Explain:

* React/Vite
* FastAPI
* SQLite
* Ollama
* open-weight models
* Quest Agent
* Vision Agent
* PWA

## Why Open Innovation Matters

This section matters.

Explain that open-weight/local AI makes it possible to:

* run inference locally
* choose/swap models
* inspect model behavior
* avoid locking the product to one provider
* keep photos/location data closer to the user
* customize models for a specific domain
* eventually move toward offline/on-device inference

Do not make vague claims.

Connect the technical architecture directly to the product.

## My Agent Session

Show how Claude Code + local model tooling helped build the project.

Include useful development observations rather than generic:

> AI helped me code faster.

Show actual agent workflow.

## Partner Technology

Explain only technologies genuinely used.

## Future

Mention:

* on-device inference
* richer personalization
* adaptive quest difficulty
* better vision verification
* offline quests
* model fine-tuning
* optional persistent memory

---

# 42. IMPORTANT PRODUCT PRINCIPLE

At every stage ask:

> Does this feature help the user go outside?

If yes:

consider it.

If no:

be skeptical.

The product should NOT become:

```text
AI chatbot
+
weather app
+
fitness tracker
+
social network
+
gamification dashboard
```

It should remain:

> **An AI-powered generator of real-world adventures.**

---

# 43. SAFETY PRINCIPLE

Generated quests must prioritize user safety.

The model should avoid suggesting:

* dangerous locations
* entering private property
* climbing
* approaching dangerous animals
* touching unknown substances
* dangerous traffic situations
* illegal activity
* risky interactions with strangers

If the model generates an unsafe quest, application-level validation should reject/regenerate it where practical.

---

# 44. MVP DEFINITION OF DONE

The MVP is done when a user can:

1. Open the app.
2. Generate a quest.
3. Read the objectives.
4. Start it.
5. See "Phone down. Go explore."
6. Go outside.
7. Take a photo.
8. Submit evidence.
9. Have an open-weight/local vision model evaluate it.
10. See accepted/rejected feedback.
11. Complete the quest.
12. Receive XP.
13. See quest history/progress.
14. Install/use the app as a PWA.
15. Understand the product without explanation.

Everything else is secondary.

---

# 45. DEADLINE PRIORITY

The challenge deadline is **October 11, 2026**.

Work backwards from the deadline.

Do NOT spend the first several days building infrastructure.

The priority order is:

```text
1. End-to-end quest loop
2. Good mobile UX
3. AI generation
4. Vision verification
5. PWA
6. Deployment
7. Voice
8. Documentation
9. Partner experiments
10. Extra polish
```

If something threatens the deadline:

CUT THE FEATURE.

Do not compromise the core loop.

---

# 46. AGENT BEHAVIOR

You are an implementation agent, not merely an advisor.

When starting:

1. Inspect the repository.
2. Inspect available skills.
3. Inspect installed tools/environment.
4. Inspect Ollama/models.
5. Create a concise implementation plan.
6. Begin implementing.

Do not ask me for permission for every small engineering decision.

Make reasonable decisions and continue.

However, when a decision materially changes the product architecture, explain the tradeoff briefly before proceeding.

---

# 47. DO NOT OVERENGINEER

Prefer:

```text
simple
working
testable
replaceable
```

over:

```text
clever
distributed
abstract
prematurely scalable
```

SQLite is enough.

A few FastAPI services are enough.

A simple agent abstraction is enough.

A simple React state machine is enough.

Do not introduce Redis, Celery, Kubernetes, vector databases, event buses, or microservices unless there is a demonstrated need.

---

# 48. UI QUALITY BAR

Do not stop when the application is merely functional.

The first version should already have:

* intentional typography
* spacing system
* consistent buttons
* strong hierarchy
* good empty states
* loading states
* subtle animations
* mobile-friendly touch targets
* visual personality

Avoid generic generated-dashboard aesthetics.

Think:

**field notebook + outdoor adventure + playful AI**

rather than:

**corporate AI SaaS**.

---

# 49. FINAL DEVELOPMENT LOOP

For every major feature:

```text
Implement
   ↓
Run
   ↓
Test
   ↓
Inspect
   ↓
Fix
   ↓
Commit
```

Do not assume code works because it looks correct.

Actually run it.

For UI work, inspect the result in a browser.

For backend work, exercise the API.

For AI work, test real model outputs.

For deployment, test the deployed application.

---

# 50. START NOW

Do not write a giant theoretical architecture document first.

Start by inspecting the repository and environment.

Then:

```text
1. Scaffold the project.
2. Get frontend + backend running.
3. Build the static mobile quest flow.
4. Wire Ollama quest generation.
5. Add SQLite.
6. Add evidence submission.
7. Add vision verification.
8. Complete the end-to-end loop.
9. Polish mobile UX.
10. Add PWA.
11. Deploy.
12. Add ElevenLabs if time allows.
13. Document everything.
```

The first objective is simple:

> **Get one person from "Start a Quest" to "Quest Complete" as quickly as possible.**

Build that loop first.

# END MASTER PROMPT
