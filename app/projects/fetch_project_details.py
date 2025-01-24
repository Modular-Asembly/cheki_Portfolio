from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict, Any
from app.models.Project import Project
from app.models.ContentElement import ContentElement
from app.modassembly.database.sql.get_sql_session import get_sql_session


def fetch_project_details(permalink: str, db: Session) -> Dict[str, Any]:
    # Retrieve project details using the permalink
    project = db.query(Project).filter(Project.permalink == permalink).one_or_none()
    if project is None:
        raise NoResultFound(f"No project found with permalink: {permalink}")

    # Retrieve associated content elements
    content_elements = db.query(ContentElement).filter(ContentElement.project_id == project.id).order_by(ContentElement.order).all()

    # Construct the detailed project content
    project_details = {
        "id": project.id.__str__(),
        "title": project.title.__str__(),
        "description": project.description.__str__(),
        "content_elements": [
            {
                "id": element.id.__str__(),
                "type": element.type.__str__(),
                "content": element.content.__str__(),
                "order": element.order.__str__()
            }
            for element in content_elements
        ]
    }

    return project_details
