from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class LessonBase(BaseModel):
    """Base model for Lesson."""
    title: str
    description: Optional[str]
    content_type: str
    access_type: str
    ordering: int
    duration: int
    published: bool

class LessonCreate(LessonBase):
    """Create model for Lesson."""
    content_url: Optional[str]
    thumbnail_url: Optional[str]
    course_id: int
    section_id: int

class LessonUpdate(BaseModel):
    """Update model for Lesson."""
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    content_type: Optional[str] = None
    access_type: Optional[str] = None
    ordering: Optional[int] = None
    duration: Optional[int] = None
    published: Optional[bool] = None

class LessonResponse(LessonBase):
    """Response model for Lesson."""
    id: int
    content_url: Optional[str]
    thumbnail_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        """ORM mode config."""
        orm_mode = True
