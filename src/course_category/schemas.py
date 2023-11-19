from typing import Optional
from pydantic import BaseModel


class CourseCategoryBase(BaseModel):
    """
    A Pydantic model for a course category.

    Attributes:
        name (str): The name of the course category.
        description (str): The description of the course category.
    """
    name: str
    description: str

class CourseCategoryCreate(CourseCategoryBase):
    """
    A Pydantic model for creating a course category.

    Attributes:
        name (str): The name of the course category.
        description (str): The description of the course category.
    """
    pass

class CourseCategoryResponse(CourseCategoryBase):
    """
    A Pydantic model for a course category
    
    Attributes:
        id (int): The id of the course category.
    """
    id: int

    class Config:
        """Pydantic ORM mode config"""
        orm_mode = True

class CourseCategoryUpdate(BaseModel):
    """
    A Pydantic model for updating a course category.

    Attributes:
        name (Optional[str]): The new name of the course category.
        description (Optional[str]): The new description of the course category.
    """
    name: Optional[str] = None
    description: Optional[str] = None