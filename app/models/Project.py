from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.modassembly.database.sql.get_sql_session import Base
from app.models.User import User


class Project(Base):
    __tablename__ = "projects"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="projects")
