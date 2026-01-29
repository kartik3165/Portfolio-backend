from fastapi import APIRouter, HTTPException
from botocore.exceptions import ClientError
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectDelete, ProjectDetail
from app.repositories.project_repo import ProjectRepo
from app.core.security import verify_passkey

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("", response_model=ProjectDetail)
def create_project(project: ProjectCreate):
    verify_passkey(project.passkey)
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
def update_project(id: str, project: ProjectUpdate):
    verify_passkey(project.passkey)
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
def delete_project(id: str, payload: ProjectDelete):
    verify_passkey(payload.passkey)
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
