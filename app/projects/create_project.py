from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict

from app.models.Project import Project
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

class ProjectCreate(BaseModel):
    title: str
    description: str
    user_id: int

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

@router.post("/projects/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_sql_session)) -> ProjectResponse:
    """
    Create a new project.

    - **title**: Title of the project
    - **description**: Description of the project
    - **user_id**: Identifier of the user who owns the project
    """
    # Validate project data
    if not project.title or not project.user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title and user_id are required.")

    # Store the project in the database
    db_project = Project(
        title=project.title,
        description=project.description,
        user_id=project.user_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return ProjectResponse(
        id=db_project.id.__int__(),
        title=db_project.title.__str__(),
        description=db_project.description.__str__(),
        user_id=db_project.user_id.__int__()
    )
