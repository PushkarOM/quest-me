# Architectural Decisions: Quest Me

## 1. Tech Stack Choices
- **React + Vite + TypeScript**: Chosen for rapid development, strong typing, and excellent PWA support.
- **FastAPI**: Chosen for its high performance, native Pydantic integration for structured AI outputs, and ease of deployment.
- **SQLite**: Chosen for the MVP to avoid the overhead of a separate database server while providing relational integrity.
- **Ollama**: Chosen to keep AI inference local and open-weight, aligning with the project's "Open Innovation" goal and ensuring privacy for user photos.

## 2. Local-First AI Strategy
- **Reasoning**: Using open-weight models ensures the project isn't locked into a single proprietary provider and allows for future on-device inference.
- **Implementation**: All model interactions go through a configurable abstraction layer in the backend.

## 3. "Screen-Light" UX
- **Reasoning**: The product's value is in the real-world experience, not the app.
- **Implementation**: Explicit "PHONE DOWN" screens and minimal, high-impact UI to encourage the user to put the device away during quests.

## 4. PWA over Native App
- **Reasoning**: Lower friction for a demo; no app store approval needed, yet provides a mobile-app-like experience with camera access and home-screen installation.

## 5. Structured AI Outputs
- **Reasoning**: LLM prose is unreliable for application state.
- **Implementation**: Mandatory JSON schemas enforced by Pydantic on the backend to ensure the frontend receives predictable data.
