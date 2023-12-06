from fastapi import HTTPException, status
from src.exceptions import AlreadyExistsException, DatabaseOperationException, NotFoundException
from .service import SectionService
from .schemas import SectionCreate, SectionUpdate



class SectionController:
    """Controller class for managing course sections."""

    @staticmethod
    def create_section(section_data: SectionCreate):
        """Controller method to create a new section."""
        try:
            return SectionService.create_section(section_data)
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except AlreadyExistsException as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    @staticmethod
    def update_section(section_id: int, update_data: SectionUpdate):
        """Controller method to update a section."""
        try:
            return SectionService.update_section(section_id, update_data)
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    @staticmethod
    def get_section(section_id: int):
        """Controller method to retrieve a section by ID."""
        try:
            return SectionService.get_section(section_id)
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
        
    @staticmethod
    def get_section_by_course_id(section_id: int, course_id: int):
        """Controller method to retrieve a section by it's course_id"""
        try:
            return SectionService.get_section_by_course_id(section_id, course_id)
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
        
    @staticmethod
    def get_sections(course_id: int):
        """Controller method to retrieve all sections."""
        try:
            return SectionService.get_sections(course_id)
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e

    @staticmethod
    def delete_section(section_id: int):
        """Controller method to delete a section."""
        try:
            SectionService.delete_section(section_id)
            return {"detail": "Section deleted successfully."}
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
        except DatabaseOperationException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
