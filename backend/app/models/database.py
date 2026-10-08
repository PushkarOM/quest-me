from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker
import datetime
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./questme.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    total_xp: Mapped[int] = mapped_column(default=0)
    streak: Mapped[int] = mapped_column(default=0)
    last_active: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc))

class Quest(Base):
    __tablename__ = "quests"
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    duration_minutes: Mapped[int] = mapped_column()
    difficulty: Mapped[str] = mapped_column()
    bonus: Mapped[Optional[str]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="GENERATED") # GENERATED, STARTED, COMPLETED
    created_at: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc))
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)
    xp_reward: Mapped[int] = mapped_column()

    objectives: Mapped[List["QuestObjective"]] = relationship(back_populates="quest")

class QuestObjective(Base):
    __tablename__ = "quest_objectives"
    id: Mapped[str] = mapped_column(primary_key=True)
    quest_id: Mapped[str] = mapped_column(ForeignKey("quests.id"))
    description: Mapped[str] = mapped_column()
    evidence_required: Mapped[bool] = mapped_column(default=True)
    status: Mapped[str] = mapped_column(default="PENDING") # PENDING, VERIFIED, REJECTED

    quest: Mapped["Quest"] = relationship(back_populates="objectives")

class Evidence(Base):
    __tablename__ = "evidence"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    objective_id: Mapped[str] = mapped_column(ForeignKey("quest_objectives.id"))
    file_path: Mapped[Optional[str]] = mapped_column(nullable=True)
    verification_status: Mapped[str] = mapped_column(default="PENDING")
    confidence: Mapped[Optional[float]] = mapped_column(nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(nullable=True)
    submitted_at: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc))

def init_db():
    Base.metadata.create_all(bind=engine)
