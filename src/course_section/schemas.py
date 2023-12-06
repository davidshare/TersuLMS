from typing import Optional
from pydantic import BaseModel


from ..model_mixins import TimestampMixin

class SectionBase(BaseModel):
    """Base schema for course sections"""
    title: str
    description: Optional[str] = None

class SectionCreate(SectionBase):
    """Schema for creating course sections"""
    course_id: int

class SectionUpdate(BaseModel):
    """Schema for updating course sections"""
    title: Optional[str] = None
    description: Optional[str] = None

class SectionResponse(SectionBase, TimestampMixin):
    """Schema for returning course sections"""
    id: int
    course_id: int
    ordering: int

    class Config:
        """Config for orm_mode"""
        orm_mode = True
