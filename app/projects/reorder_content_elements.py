from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.models.ContentElement import ContentElement
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

class ContentElementOrder(BaseModel):
    id: int
    order: int

class ReorderResponse(BaseModel):
    success: bool
    message: str

@router.put("/projects/{project_id}/content/reorder", response_model=ReorderResponse)
def reorder_content_elements(
    project_id: int,
    content_orders: List[ContentElementOrder],
    db: Session = Depends(get_sql_session)
) -> ReorderResponse:
    """
    Reorder content elements for a given project.

    - **project_id**: ID of the project whose content elements are to be reordered.
    - **content_orders**: List of content element IDs and their new order.

    Returns a success message if the reordering is successful.
    """
    # Retrieve content elements by project ID
    content_elements = db.query(ContentElement).filter(ContentElement.project_id == project_id).all()

    if not content_elements:
        raise HTTPException(status_code=404, detail="Project or content elements not found.")

    # Update order of content elements
    for content_order in content_orders:
        for element in content_elements:
            if element.id == content_order.id:
                element.order = content_order.order

    # Save changes to the database
    db.commit()

    return ReorderResponse(success=True, message="Content elements reordered successfully.")
