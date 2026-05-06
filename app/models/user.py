from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    email: EmailStr = Field(..., unique=True)
    hashed_password: str
    is_active: bool = True
    refresh_token: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
        indexes = ["email"]
