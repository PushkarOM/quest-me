import os
import shutil
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

from app.models.database import SessionLocal, engine, Base, init_db, User, Quest, QuestObjective, Evidence
from app.services.inference import get_inference_provider, BaseInferenceProvider
from app.services.vision import get_vision_provider, VisionProvider

load_dotenv()

# Initialize Database
init_db()

app = FastAPI(title="Quest Me API")

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
    description: str
    evidence_required: bool = True

class QuestSchema(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    duration_minutes: int
    difficulty: str
    objectives: List[ObjectiveSchema]
    bonus: Optional[str] = None
    xp: int

# --- AI Logic ---

def generate_quest_via_provider(provider: BaseInferenceProvider, theme: str = "Urban Naturalist") -> QuestSchema:
    prompt = f"""
    You are the Quest Me Quest Agent. Generate a real-world outdoor adventure quest.
    Theme: {theme}

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
        return QuestSchema.model_validate(data)
    except Exception as e:
        print(f"Error generating quest: {e}")
        raise HTTPException(status_code=500, detail=f"AI Generation failed: {str(e)}")

# --- Endpoints ---

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Quest Me API is running"}

@app.post("/api/quests/generate", response_model=QuestSchema)
async def generate_quest(theme: Optional[str] = "Urban Naturalist", db: Session = Depends(get_db)):
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
        xp_reward=quest_data.xp,
        status="GENERATED"
    )
    db.add(db_quest)

    for obj in quest_data.objectives:
        # Use a combined ID to ensure uniqueness across different quests
        db_obj = QuestObjective(
            id=f"{quest_id}_{obj.id}",
            quest_id=quest_id,
            description=obj.description,
            evidence_required=obj.evidence_required
        )
        db.add(db_obj)


    db.commit()
    return {**quest_data.model_dump(), "id": quest_id}

@app.post("/api/quests/{quest_id}/start")
async def start_quest(quest_id: str, db: Session = Depends(get_db)):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    quest.status = "STARTED"
    db.commit()
    return {"status": "STARTED", "message": "Phone down. Go explore!"}

@app.post("/api/quests/{quest_id}/objectives/{objective_id}/evidence")
async def submit_evidence(
    quest_id: str,
    objective_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Validate Objective
    obj = db.query(QuestObjective).filter(
        QuestObjective.id == objective_id,
        QuestObjective.quest_id == quest_id
    ).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Objective not found")

    # 2. Save File Temporarily
    file_path = os.path.join(UPLOAD_DIR, f"{objective_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Vision Verification
    vision_provider = get_vision_provider()
    with open(file_path, "rb") as f:
        image_bytes = f.read()

    verification = vision_provider.verify_evidence(image_bytes, obj.description)

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

    # Cleanup temporary file (as per privacy principle in master prompt)
    # os.remove(file_path)

    return {
        "valid": verification["valid"],
        "reason": verification["reason"],
        "confidence": verification.get("confidence")
    }

@app.post("/api/quests/{quest_id}/complete")
async def complete_quest(quest_id: str, db: Session = Depends(get_db)):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    # Check if all required objectives are verified
    objectives = db.query(QuestObjective).filter(QuestObjective.quest_id == quest_id).all()
    all_done = all(obj.status == "VERIFIED" for obj in objectives if obj.evidence_required)

    if not all_done:
        raise HTTPException(status_code=400, detail="Not all objectives verified")

    quest.status = "COMPLETED"
    quest.completed_at = datetime.datetime.utcnow()

    # Award XP
    user = db.query(User).filter(User.id == quest.user_id).first()
    user.total_xp += quest.xp_reward

    db.commit()
    return {"status": "COMPLETED", "total_xp": user.total_xp}
