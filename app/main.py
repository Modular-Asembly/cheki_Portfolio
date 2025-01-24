from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers

from app.models.Project import Project
from app.models.User import User
from app.models.ContentElement import ContentElement
from app.auth.create_user import router
app.include_router(router)
from app.auth.authenticate_user import router
app.include_router(router)
from app.projects.create_project import router
app.include_router(router)
from app.projects.update_project import router
app.include_router(router)
from app.projects.reorder_content_elements import router
app.include_router(router)
from app.projects.upload_image import router
app.include_router(router)
from app.auth.login import router
app.include_router(router)
from app.cms.manage_projects import router
app.include_router(router)
from app.cms.manage_project_content import router
app.include_router(router)
from app.app.display_project_listings import router
app.include_router(router)
from app.app.display_project_details import router
app.include_router(router)

# Database

from app.modassembly.database.sql.get_sql_session import Base, engine
Base.metadata.create_all(engine)
