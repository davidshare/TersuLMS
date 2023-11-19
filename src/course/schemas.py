from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseCreate(BaseModel):
    """Course Schema"""
    title: str
    slug: str
    description: str
    course_level: str
    course_language: str
    course_duration: int
    course_thumbnail: str
    author_id: int
    course_category_id: int
    price: float


class UpdateCourse(BaseModel):
    """Update Course Schema"""
    id: Optional[int] = None
    course_category_id: Optional[int] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    course_level: Optional[str] = None
    course_language: Optional[str] = None
    course_duration: Optional[int] = None
    course_thumbnail: Optional[str] = None
    author_id: Optional[int] = None
    published: Optional[bool] = False
    published_at: Optional[datetime] = None
    

    class Config:
        """Pydantic ORM mode config"""
        orm_mode = True


class CourseResponse(CourseCreate):
    """Course Response Schema"""
    id: int
    published: bool
    published_at: datetime

    class Config:
        """Pydantic ORM mode config"""
        orm_mode = True
