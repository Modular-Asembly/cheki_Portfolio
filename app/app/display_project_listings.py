from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.projects.fetch_projects import fetch_projects
from app.models.Project import Project
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

class ProjectListing(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

@router.get("/", response_model=List[ProjectListing])
def display_project_listings(db: Session = Depends(get_sql_session)) -> List[ProjectListing]:
    """
    Retrieve and display all project listings.

    Returns a list of projects with their details.
    """
    projects = fetch_projects()

    return [
        ProjectListing(
            id=project.id.__int__(),
            title=project.title.__str__(),
            description=project.description.__str__(),
            user_id=project.user_id.__int__()
        )
        for project in projects
    ]
