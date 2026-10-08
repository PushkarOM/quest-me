# 🌿 Quest Me: Turning the Real World into a Quest Log

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built
**Quest Me** is an AI-powered outdoor adventure PWA designed with a single philosophy: *"The AI generates the adventure. The human lives it."*

Unlike most AI apps that keep you glued to the screen, Quest Me uses AI to push you away from it. It generates unique, safe, and physically possible "Field Quests" (like *Urban Naturalist* or *Architectural Eye*) that challenge users to observe the ordinary details of their environment that most people walk past.

**How it gets people outside:**
1. **The Briefing**: The AI generates a mission with 3 specific observable objectives.
2. **The Commitment**: Once the user accepts the quest, the app enters **Field Mode**, explicitly instructing the user to put their phone in their pocket.
3. **The Evidence**: Users only retrieve their device to capture photo evidence of their findings.
4. **Vision Verification**: An open-weight vision model analyzes the photos to verify the find, awarding XP and streaks upon completion.

It's for the curious, the urban explorers, and anyone who needs a digital nudge to actually touch grass.

## Demo
**Live App**: [https://quest-me-frontend.onrender.com](https://quest-me-frontend.onrender.com)

## Code
**GitHub Repository**: [https://github.com/PushkarOM/quest-me](https://github.com/PushkarOM/quest-me)

## How I Built It
Quest Me is built as a hardened MVP focusing on a tight vertical slice of "Generate $\rightarrow$ Explore $\rightarrow$ Verify."

**The Stack:**
- **Frontend**: React 19, Vite, and TypeScript. I implemented a custom **"Field Notebook" Design System** using Tailwind v4, utilizing a cream-and-sage palette and distressed textures to make the app feel like a physical expedition log rather than a SaaS product.
- **Backend**: Python with FastAPI and SQLAlchemy 2.0, using SQLite for lightweight, local-first persistence.
- **AI Engine**: Powered by **Ollama** running on a private, self-managed Ubuntu server.
    - **Quest Generation**: Used structured JSON output via `qwen2.5-coder:3b` to ensure the AI consistently generates valid quests with balanced difficulty and XP.
    - **Evidence Verification**: Integrated the `llava` vision model to perform real-time verification of photo evidence.
- **PWA**: Integrated a Service Worker and Web Manifest to allow the app to be installed on mobile devices for a truly standalone "field" experience.

## Why Does Open Innovation Matter?
Open innovation is the heartbeat of Quest Me. By hosting my own AI infrastructure via Ollama on a private server, I achieved several critical goals:

1. **Absolute Privacy**: All photo evidence is processed on a private server. There is no third-party corporate API seeing where the user is or what they are photographing.
2. **Infrastructure Independence**: The app is not dependent on expensive API credits or the whims of a closed-provider's pricing model.
3. **Fail-Closed Reliability**: I could tune the vision verification prompts and structured output constraints to ensure the AI won't just "hallucinate" a success; it requires genuine evidence.
4. **Edge-Ready**: This architecture proves that complex vision-AI workflows can be decoupled from "Big Tech" clouds and run on accessible, private hardware.

## My Agent Session
[Insert DevRelay Agent Session Link Here]

## Prize Categories
- **Best Use of Open-Weight Models**
- **Most Innovative "Touch Grass" Implementation**
