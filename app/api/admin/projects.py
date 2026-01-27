from fastapi import APIRouter, HTTPException
from botocore.exceptions import ClientError
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectDelete, ProjectDetail
from app.repositories.project_repo import ProjectRepo

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

from app.core.security import get_current_admin
from fastapi import Depends

@router.post("", response_model=ProjectDetail)
def create_project(project: ProjectCreate, admin: dict = Depends(get_current_admin)):
    repo = ProjectRepo()
    try:
        return repo.create_project(project.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
             raise HTTPException(status_code=409, detail="Project already exists")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}", response_model=ProjectDetail)
def update_project(id: str, project: ProjectUpdate, admin: dict = Depends(get_current_admin)):
    repo = ProjectRepo()
    try:
        updated = repo.update_project(id, project.model_dump())
        if not updated:
             raise HTTPException(status_code=404, detail="Project not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
             raise HTTPException(status_code=404, detail="Project not found")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}")
def delete_project(id: str, admin: dict = Depends(get_current_admin)):
    repo = ProjectRepo()
    try:
        repo.delete_project(id)
        return {"message": "Project deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
             raise HTTPException(status_code=404, detail="Project not found")
        raise HTTPException(status_code=400, detail=str(e))
