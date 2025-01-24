from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any, Dict
from app.projects.fetch_project_details import fetch_project_details
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

class ProjectDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    content_elements: Any

@router.get("/project/{permalink}", response_model=ProjectDetailResponse)
def display_project_details(permalink: str, db: Session = Depends(get_sql_session)) -> ProjectDetailResponse:
    """
    Retrieve and display detailed project content by permalink.

    - **permalink**: The permalink of the project to retrieve.

    Returns the detailed project content.
    """
    try:
        project_details = fetch_project_details(permalink, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return ProjectDetailResponse(**project_details)
