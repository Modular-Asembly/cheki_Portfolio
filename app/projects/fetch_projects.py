from typing import List
from sqlalchemy.orm import Session
from app.models.Project import Project
from app.modassembly.database.sql.get_sql_session import get_sql_session


def fetch_projects() -> List[Project]:
    with get_sql_session() as session:
        projects = session.query(Project).all()
        return projects
