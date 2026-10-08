# 🌿 Quest Me
**"The AI generates the adventure. The human lives it."**

Quest Me is an AI-powered outdoor adventure PWA that turns the real world into a quest log. It uses local LLMs (via Ollama) to generate quests and vision models to verify evidence through photos.

## 🚀 Quick Start

### 🛠️ Backend Setup
1. `cd backend`
2. `python -m venv venv`
3. `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
4. `pip install -r requirements.txt`
5. Create a `.env` file in `backend/` with:
   `OLLAMA_BASE_URL=http://localhost:11434`
   `VISION_MODEL=llava`
6. `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### 🎨 Frontend Setup
1. `cd frontend`
2. `npm install`
3. Create a `.env` file in `frontend/` with:
   `VITE_API_BASE=http://localhost:8000` (Replace with your public tunnel URL for mobile testing)
4. `npm run dev`

## 🏗️ Architecture
- **Frontend**: React 19, Vite, TypeScript, Tailwind v4 (Field Notebook Design System).
- **Backend**: FastAPI, SQLAlchemy 2.0, SQLite.
- **AI Engine**: Ollama (Local-first) for quest generation and vision verification.
- **PWA**: Manifest and Service Worker integrated for standalone mobile experience.

## 📖 Core Loop
`Generate Quest` $\rightarrow$ `Start Quest` $\rightarrow$ `Phone Down / Field Mode` $\rightarrow$ `Photo Evidence` $\rightarrow$ `Vision Verification` $\rightarrow$ `XP & Streaks`.

## 🛡️ Security & Privacy
- **Privacy by Design**: Uploaded photos are processed in memory and deleted immediately after verification.
- **Fail-Closed**: AI verification defaults to rejected on error.
- **Rate Limited**: Protection against AI provider abuse.
