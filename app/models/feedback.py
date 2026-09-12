from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class Feedback(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = Field(default=None, max_length=100)
    email: Optional[EmailStr] = None
    message: str = Field(min_length=1, max_length=2000)
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    created_at: Optional[str] = None


class ContactSubmission(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=1, max_length=150)
    message: str = Field(min_length=1, max_length=2000)
    created_at: Optional[str] = None
