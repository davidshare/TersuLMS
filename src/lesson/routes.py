from fastapi import APIRouter, status

from .controller import LessonController
from .schemas import ArticleContentResponse, ArticleContentUpdate, FileContentResponse, FileContentUpdate, LessonCreate, LessonResponse, LessonUpdate

router = APIRouter()

@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_lesson(lesson_data: LessonCreate):
    """Handles creating lessons"""
    return LessonController.create_lesson(lesson_data)

@router.get("/id/{lesson_id}", response_model=LessonResponse)
def get_lesson_by_id(lesson_id: int):
    """Handles getting lesson by id"""
    return LessonController.get_lesson_by_id(lesson_id)

@router.put("/id/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, lesson_data: LessonUpdate):
    """Handles updating lesson by id"""
    return LessonController.update_lesson(lesson_id, lesson_data)

@router.put("/file-content/id/{file_content_id}", response_model=FileContentResponse)
def update_file_content(file_content_id: int, file_content: FileContentUpdate):
    """
    Handles updating file content

    Args:
        file_content_id (int): File content id
        file_content (FileContent): File content data

    Returns:
        Filecontent: Filecontent object
    """
    return LessonController.update_file_content(file_content_id, file_content)

@router.put("/article-content/id/{article_content_id}", response_model=ArticleContentResponse)
def update_article_content(article_content_id: int, article_content: ArticleContentUpdate):
    """
    Handles updating article content

    Args:
        article_content_id (int): Article content id
        article_content (ArticleContent): Article content data

    Returns:
        ArticleContent: ArticleContent object
    """
    return LessonController.update_article_content(article_content_id, article_content)

@router.delete("/id/{lesson_id}")
def delete_lesson(lesson_id: int):
    """Handles deleting lesson by id"""
    return LessonController.delete_lesson(lesson_id)
