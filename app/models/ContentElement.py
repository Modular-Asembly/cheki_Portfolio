from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.modassembly.database.sql.get_sql_session import Base
from app.models.Project import Project


class ContentElement(Base):
    __tablename__ = "content_elements"

    id: int = Column(Integer, primary_key=True, index=True)
    project_id: int = Column(Integer, ForeignKey("projects.id"), nullable=False)
    type: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    order: int = Column(Integer, nullable=False)

    project = relationship("Project", back_populates="content_elements")
