from sqlalchemy.orm import Session
from app.models.ContentElement import ContentElement
from app.modassembly.database.sql.get_sql_session import get_sql_session


def add_content_element(session: Session, project_id: int, content_type: str, content: str, order: int) -> ContentElement:
    # Validate content element data
    if not content_type or not content:
        raise ValueError("Content type and content must be provided.")

    # Create a new ContentElement instance
    new_content_element = ContentElement(
        project_id=project_id,
        type=content_type.__str__(),
        content=content.__str__(),
        order=order
    )

    # Store the content element in the database
    session.add(new_content_element)
    session.commit()
    session.refresh(new_content_element)

    return new_content_element
