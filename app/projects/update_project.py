from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict
from app.models.Project import Project
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

class ProjectUpdateRequest(BaseModel):
    title: str
    description: str

class ProjectUpdateResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

@router.put("/projects/{project_id}", response_model=ProjectUpdateResponse)
def update_project(project_id: int, project_data: ProjectUpdateRequest, db: Session = Depends(get_sql_session)) -> ProjectUpdateResponse:
    """
    Update project details by project ID.

    - **project_id**: The ID of the project to update.
    - **project_data**: The new data for the project, including title and description.

    Returns the updated project details.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.title = project_data.title
    project.description = project_data.description
    db.commit()
    db.refresh(project)

    return ProjectUpdateResponse(
        id=project.id.__int__(),
        title=project.title.__str__(),
        description=project.description.__str__(),
        user_id=project.user_id.__int__()
    )
