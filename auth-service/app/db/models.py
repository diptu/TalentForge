# app/db/models.py
from datetime import datetime
import enum

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Enum
from app.db.base import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: "Column[int]" = Column(Integer, primary_key=True, index=True)
    email: "Column[str]" = Column(String, unique=True, index=True, nullable=False)
    hashed_password: "Column[str]" = Column(String, nullable=False)

    # ✅ Fix here
    role: "Column[UserRole]" = Column(
        Enum(UserRole), default=UserRole.USER, nullable=False
    )

    is_active: "Column[bool]" = Column(Boolean, default=True, nullable=False)
    is_superuser: "Column[bool]" = Column(Boolean, default=False, nullable=False)
    created_at: "Column[datetime]" = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: "Column[datetime]" = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
