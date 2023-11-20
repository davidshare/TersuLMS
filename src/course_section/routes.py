from fastapi import APIRouter, status
from .controller import SectionController
from .schemas import SectionCreate, SectionUpdate, SectionResponse

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=SectionResponse)
def create_section(section: SectionCreate):
    """API endpoint to create a new section."""
    return SectionController.create_section(section)


@router.get("/id/{section_id}", status_code=status.HTTP_200_OK, response_model=SectionResponse)
def get_section(section_id: int):
    """API endpoint to get a section by id."""
    return SectionController.get_section(section_id)

@router.get("/section/{section_id}/course/{course_id}", status_code=status.HTTP_200_OK, response_model=SectionResponse)
def get_section_by_course_section(section_id: int, course_id: int):
    """API endpoint to get a section by id."""
    return SectionController.get_section_by_course_id(section_id, course_id)


@router.get("/{course_id}", status_code=status.HTTP_200_OK, response_model=list[SectionResponse])
def get_sections(course_id: int):
    """API endpoint to get all sections."""
    return SectionController.get_sections(course_id)


@router.put("/{section_id}", status_code=status.HTTP_200_OK, response_model=SectionResponse)
def update_section(section_id: int, section: SectionUpdate):
    """API endpoint to update a section by id."""
    return SectionController.update_section(section_id, section)


@router.delete("/{section_id}", status_code=status.HTTP_200_OK)
def delete_section(section_id: int):
    """API endpoint to delete a section by id."""
    return SectionController.delete_section(section_id)
