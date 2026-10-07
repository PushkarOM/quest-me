# Architecture: Quest Me

## High-Level Flow
`User` ↔ `PWA (React)` ↔ `Backend (FastAPI)` ↔ `AI Agents (Ollama)` ↔ `Database (SQLite)`

## Component Breakdown

### 1. Frontend (PWA)
- **Stack**: React + Vite + TypeScript.
- **Responsibilities**: 
  - Mobile-first UI/UX.
  - PWA manifest and service workers for installability.
  - Camera API integration for evidence submission.
  - Local state management for the quest state machine.

### 2. Backend (FastAPI)
- **Stack**: Python + FastAPI + Pydantic.
- **Responsibilities**:
  - Orchestrate AI agent calls.
  - Manage quest state transitions.
  - Handle photo uploads and temporary storage for verification.
  - Manage user progress and XP in SQLite.

### 3. AI Layer (Ollama)
- **Quest Agent**: Generates structured JSON quests based on theme/context.
- **Vision Agent**: Evaluates evidence photos against quest objectives.
- **Config**: Model names are environment-driven (`QUEST_MODEL`, `VISION_MODEL`).

### 4. Data Layer (SQLite)
- **Schema**:
  - `users`: Basic profile and total XP.
  - `quests`: Generated quest metadata and global state.
  - `quest_objectives`: Individual goals per quest and their verification state.
  - `evidence`: Metadata linking photos to objectives.
  - `progress`: Streak and history tracking.

## State Machine
- **Quest States**: `GENERATED` → `STARTED` → `IN_PROGRESS` → `EVIDENCE_SUBMITTED` → `VERIFIED` → `COMPLETED`.
- **Objective States**: `PENDING` → `EVIDENCE_SUBMITTED` → `VERIFIED` | `REJECTED`.
