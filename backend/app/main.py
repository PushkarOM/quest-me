import os
import shutil
import logging
import random
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("questme")

from app.models.database import SessionLocal, engine, Base, init_db, User, Quest, QuestObjective, Evidence
from app.services.inference import get_inference_provider, BaseInferenceProvider
from app.services.vision import get_vision_provider, VisionProvider

load_dotenv()

# Initialize Database
init_db()

# Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Quest Me API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Setup upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Schemas ---

class ObjectiveSchema(BaseModel):
    id: str
    description: str = Field(..., min_length=1, max_length=200)
    evidence_required: bool = True
    status: str = "PENDING"

class QuestSchema(BaseModel):
    id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=80)
    description: str = Field(..., min_length=1, max_length=400)
    duration_minutes: int = Field(..., ge=5, le=60)
    difficulty: str = Field(...) # Handled via Literal/Normalization in provider
    objectives: List[ObjectiveSchema] = Field(..., min_length=1, max_length=5)
    bonus: Optional[str] = Field(None, max_length=160)
    xp: int

class UserSchema(BaseModel):
    total_xp: int
    streak: int
    completed_quests: int

# --- AI Logic ---

def generate_quest_via_provider(provider: BaseInferenceProvider, theme: str = "Urban Naturalist") -> QuestSchema:
    # Expanded themes to move beyond just "Urban Naturalist"
    themes = [
        "Urban Naturalist (find greenery in the city)",
        "Architectural Eye (find unique building details)",
        "Soundscape Hunter (find specific ambient sounds)",
        "Texture Collector (find contrasting tactile surfaces)",
        "Color Quest (find items of a specific rare color)"
    ]
    selected_theme = random.choice(themes) if theme == "Urban Naturalist" else theme

    prompt = f"""
    You are the Quest Me Quest Agent. Generate a real-world outdoor adventure quest.
    Theme: {selected_theme}

    The quest must be:
    - Physically possible and safe.
    - Short (15-30 mins).
    - Location-flexible (work in most urban/suburban areas).
    - Focused on observing the physical world.

    Return ONLY valid JSON matching this schema:
    {{
      "title": "Quest Title",
      "description": "Quest description...",
      "duration_minutes": 20,
      "difficulty": "easy",
      "objectives": [
        {{ "id": "obj_1", "description": "Find X...", "evidence_required": true }}
      ],
      "bonus": "Optional bonus challenge",
      "xp": 100
    }}
    """
    try:
        data = provider.generate_json(prompt, "QuestSchema")
        validated = QuestSchema.model_validate(data)

        # Server-Authoritative XP: Ignore LLM's xp value
        difficulty_map = {"easy": 50, "medium": 100, "hard": 150}
        diff_lower = validated.difficulty.lower()
        validated.xp = difficulty_map.get(diff_lower, 50)

        return validated
    except Exception as e:
        logger.error(f"AI Generation failed: {e}")
        raise HTTPException(status_code=502, detail="The quest generator is unavailable, try again")

# --- Endpoints ---

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Quest Me API is running"}

@app.get("/api/me", response_model=UserSchema)
async def get_me(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(id=1, username="demo_user", total_xp=0, streak=0)
        db.add(user)
        db.commit()

    completed_count = db.query(Quest).filter(Quest.user_id == user.id, Quest.status == "COMPLETED").count()
    return UserSchema(total_xp=user.total_xp, streak=user.streak, completed_quests=completed_count)

@app.get("/api/quests/active")
async def get_active_quest(db: Session = Depends(get_db)):
    # Find the most recent non-completed quest for demo user
    quest = db.query(Quest).filter(Quest.user_id == 1, Quest.status != "COMPLETED").order_by(Quest.created_at.desc()).first()
    if not quest:
        return None

    objectives = db.query(QuestObjective).filter(QuestObjective.quest_id == quest.id).all()
    obj_list = [ObjectiveSchema(id=o.id, description=o.description, evidence_required=o.evidence_required, status=o.status) for o in objectives]

    return {
        "id": quest.id,
        "title": quest.title,
        "description": quest.description,
        "duration_minutes": quest.duration_minutes,
        "difficulty": quest.difficulty,
        "objectives": obj_list,
        "bonus": quest.bonus, # Note: bonus needs to be added to Quest model
        "xp": quest.xp_reward,
        "status": quest.status
    }

@app.get("/api/quests/{quest_id}")
async def get_quest(quest_id: str, db: Session = Depends(get_db)):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    objectives = db.query(QuestObjective).filter(QuestObjective.quest_id == quest.id).all()
    obj_list = [ObjectiveSchema(id=o.id, description=o.description, evidence_required=o.evidence_required, status=o.status) for o in objectives]

    return {
        "id": quest.id,
        "title": quest.title,
        "description": quest.description,
        "duration_minutes": quest.duration_minutes,
        "difficulty": quest.difficulty,
        "objectives": obj_list,
        "bonus": None, # Placeholder until model updated
        "xp": quest.xp_reward,
        "status": quest.status
    }

@app.post("/api/quests/generate", response_model=QuestSchema)
@limiter.limit("5/hour")
async def generate_quest(request: Request, theme: Optional[str] = "Urban Naturalist", db: Session = Depends(get_db)):
    provider = get_inference_provider()
    quest_data = generate_quest_via_provider(provider, theme)

    demo_user = db.query(User).filter(User.id == 1).first()
    if not demo_user:
        demo_user = User(id=1, username="demo_user", total_xp=0)
        db.add(demo_user)
        db.commit()

    import uuid
    quest_id = str(uuid.uuid4())
    db_quest = Quest(
        id=quest_id,
        user_id=demo_user.id,
        title=quest_data.title,
        description=quest_data.description,
        duration_minutes=quest_data.duration_minutes,
        difficulty=quest_data.difficulty,
        bonus=quest_data.bonus,
        xp_reward=quest_data.xp,
        status="GENERATED"
    )
    db.add(db_quest)

    for obj in quest_data.objectives:
        # Use a server-generated ID to ensure uniqueness and authority
        import uuid
        obj_id = str(uuid.uuid4())
        db_obj = QuestObjective(
            id=obj_id,
            quest_id=quest_id,
            description=obj.description,
            evidence_required=obj.evidence_required
        )
        db.add(db_obj)
        # Update the quest_data object to return the real DB ID to the client
        for i, item in enumerate(quest_data.objectives):
            if item.id == obj.id:
                quest_data.objectives[i].id = obj_id
                break

    db.commit()
    return {**quest_data.model_dump(), "id": quest_id}

@app.post("/api/quests/{quest_id}/start")
async def start_quest(quest_id: str, db: Session = Depends(get_db)):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    if quest.status == "COMPLETED":
        raise HTTPException(status_code=409, detail="Quest already completed")
    quest.status = "STARTED"
    db.commit()
    return {"status": "STARTED", "message": "Phone down. Go explore!"}

@app.post("/api/quests/{quest_id}/objectives/{objective_id}/evidence")
@limiter.limit("10/minute")
async def submit_evidence(
    request: Request,
    quest_id: str,
    objective_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Validate Quest State
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    if quest.status != "STARTED":
        raise HTTPException(status_code=409, detail="Evidence can only be submitted for STARTED quests")

    # 2. Validate Objective
    obj = db.query(QuestObjective).filter(
        QuestObjective.id == objective_id,
        QuestObjective.quest_id == quest_id
    ).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objective not found")

    # 2. Save File Temporarily
    # Security: Validate file size before saving (Max 8MB)
    MAX_FILE_SIZE = 8 * 1024 * 1024
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 8MB.")

    file_path = os.path.join(UPLOAD_DIR, f"{objective_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # 3. Vision Verification
    vision_provider = get_vision_provider()
    # Use the already read content from memory instead of re-reading from disk
    verification = vision_provider.verify_evidence(content, obj.description)

    # 4. Update DB
    evidence = Evidence(
        objective_id=objective_id,
        file_path=file_path,
        verification_status="VERIFIED" if verification["valid"] else "REJECTED",
        confidence=verification.get("confidence"),
        reason=verification.get("reason")
    )
    db.add(evidence)

    if verification["valid"]:
        obj.status = "VERIFIED"
    else:
        obj.status = "REJECTED"

    db.commit()

    # Security: Cleanup temporary file immediately after verification to preserve privacy
    try:
        os.remove(file_path)
    except OSError as e:
        logger.warning(f"Failed to remove temporary file {file_path}: {e}")

    return {
        "valid": verification["valid"],
        "reason": verification["reason"],
        "confidence": verification.get("confidence")
    }

@app.post("/api/quests/{quest_id}/complete")
async def complete_quest(quest_id: str, db: Session = Depends(get_db)):
    # Atomic update to prevent double-claiming XP
    result = db.query(Quest).filter(Quest.id == quest_id, Quest.status == "STARTED").update({"status": "COMPLETED", "completed_at": datetime.now(timezone.utc)})
    if result == 0:
        quest = db.query(Quest).filter(Quest.id == quest_id).first()
        if not quest:
            raise HTTPException(status_code=404, detail="Quest not found")
        if quest.status == "COMPLETED":
            raise HTTPException(status_code=409, detail="Quest already completed")
        raise HTTPException(status_code=400, detail="Quest must be STARTED before completion")

    # Check if all required objectives are verified
    objectives = db.query(QuestObjective).filter(QuestObjective.quest_id == quest_id).all()
    all_done = all(obj.status == "VERIFIED" for obj in objectives if obj.evidence_required)

    if not all_done:
        # Rollback status if not all objectives are done
        db.query(Quest).filter(Quest.id == quest_id).update({"status": "STARTED"})
        db.commit()
        raise HTTPException(status_code=400, detail="Not all objectives verified")

    # Award XP
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    user = db.query(User).filter(User.id == quest.user_id).first()
    user.total_xp += quest.xp_reward

    # Update streak
    now = datetime.now(timezone.utc).date()
    if user.last_active:
        last_date = user.last_active.date()
        if (now - last_date).days == 1:
            user.streak += 1
        elif (now - last_date).days > 1:
            user.streak = 1
    else:
        user.streak = 1
    user.last_active = datetime.now(timezone.utc)

    db.commit()
    return {"status": "COMPLETED", "xp_awarded": quest.xp_reward, "total_xp": user.total_xp, "streak": user.streak}
