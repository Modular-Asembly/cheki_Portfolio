from sqlalchemy.orm import Session
from app.models.Project import Project
from app.modassembly.database.sql.get_sql_session import get_sql_session


def delete_project(project_id: int) -> None:
    with next(get_sql_session()) as db:  # type: Session
        project: Project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            db.delete(project)
            db.commit()
