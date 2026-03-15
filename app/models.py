from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Auth ──────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Contact ───────────────────────────────────────
class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class ContactResponse(BaseModel):
    id: str
    created_at: datetime
    status: str = "received"


# ── Projects ──────────────────────────────────────
class ProjectView(BaseModel):
    project_id: str
    views: int


# ── Blog ──────────────────────────────────────────
class PostCreate(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    published: bool = False
    tags: Optional[list[str]] = []


class PostUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    tags: Optional[list[str]] = None


class Post(BaseModel):
    id: str
    title: str
    slug: str
    excerpt: str
    content: str
    published: bool
    tags: list[str]
    created_at: datetime
    updated_at: datetime
