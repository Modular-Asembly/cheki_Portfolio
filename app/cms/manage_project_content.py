from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Union
from pydantic import BaseModel
from app.projects.add_content_element import add_content_element
from app.projects.reorder_content_elements import reorder_content_elements, ContentElementOrder, ReorderResponse
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

class ContentElementCreate(BaseModel):
    project_id: int
    type: str
    content: str
    order: int

class ContentElementResponse(BaseModel):
    id: int
    project_id: int
    type: str
    content: str
    order: int

@router.post("/cms/project/content", response_model=ContentElementResponse)
def add_content(request: ContentElementCreate, db: Session = Depends(get_sql_session)) -> ContentElementResponse:
    """
    Add a new content element to a project.

    - **project_id**: ID of the project to add content to.
    - **type**: Type of the content (e.g., paragraph, image).
    - **content**: The actual content or reference to the content.
    - **order**: Order of the content element within the project.

    Returns the added content element.
    """
    new_content = add_content_element(db, request.project_id, request.type, request.content, request.order)
    return ContentElementResponse(
        id=new_content.id.__int__(),
        project_id=new_content.project_id.__int__(),
        type=new_content.type.__str__(),
        content=new_content.content.__str__(),
        order=new_content.order.__int__()
    )

@router.put("/cms/project/content/reorder", response_model=ReorderResponse)
def reorder_content(request: List[ContentElementOrder], db: Session = Depends(get_sql_session)) -> ReorderResponse:
    """
    Reorder content elements for a project.

    - **request**: List of content element IDs and their new order.

    Returns a success message if the reordering is successful.
    """
    return reorder_content_elements(request, db)
