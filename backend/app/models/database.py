from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./questme.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    total_xp = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)

class Quest(Base):
    __tablename__ = "quests"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    duration_minutes = Column(Integer)
    difficulty = Column(String)
    status = Column(String, default="GENERATED") # GENERATED, STARTED, COMPLETED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    xp_reward = Column(Integer)

    objectives = relationship("QuestObjective", back_populates="quest")

class QuestObjective(Base):
    __tablename__ = "quest_objectives"
    id = Column(String, primary_key=True)
    quest_id = Column(String, ForeignKey("quests.id"))
    description = Column(String)
    evidence_required = Column(Boolean, default=True)
    status = Column(String, default="PENDING") # PENDING, SUBMITTED, VERIFIED, REJECTED

    quest = relationship("Quest", back_populates="objectives")

class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(Integer, primary_key=True, index=True)
    objective_id = Column(String, ForeignKey("quest_objectives.id"))
    file_path = Column(String)
    verification_status = Column(String, default="PENDING")
    confidence = Column(Float, nullable=True)
    reason = Column(String, nullable=True)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
