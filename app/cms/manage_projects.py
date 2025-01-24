from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Any
from app.projects.create_project import create_project
from app.projects.update_project import update_project
from app.projects.delete_project import delete_project
from app.modassembly.database.sql.get_sql_session import get_sql_session

router = APIRouter()

@router.api_route("/cms/projects", methods=["POST", "PUT", "DELETE"])
async def manage_projects(request: Request, db: Session = Depends(get_sql_session)) -> Any:
    """
    Manage projects by handling HTTP requests for creation, updating, and deletion.

    - **POST**: Create a new project.
    - **PUT**: Update an existing project.
    - **DELETE**: Delete a project.

    Returns a JSON response with the result of the operation.
    """
    if request.method == "POST":
        project_data = await request.json()
        return create_project(project_data, db)

    elif request.method == "PUT":
        project_data = await request.json()
        project_id = project_data.get("id")
        if not project_id:
            raise HTTPException(status_code=400, detail="Project ID is required for update.")
        return update_project(project_id, project_data, db)

    elif request.method == "DELETE":
        project_data = await request.json()
        project_id = project_data.get("id")
        if not project_id:
            raise HTTPException(status_code=400, detail="Project ID is required for deletion.")
        delete_project(project_id, db)
        return JSONResponse(content={"message": "Project deleted successfully."})

    raise HTTPException(status_code=405, detail="Method not allowed.")
