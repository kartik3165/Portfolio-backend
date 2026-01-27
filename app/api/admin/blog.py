from fastapi import APIRouter, HTTPException, Depends
from botocore.exceptions import ClientError

from app.schemas.blog import BlogCreate, BlogDelete, BlogDetail, BlogUpdate
from app.repositories.blog_repo import BlogRepo
from app.core.security import get_current_admin

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@router.post("", response_model=BlogDetail)
async def create_blog(data: BlogCreate, admin: dict = Depends(get_current_admin)):
    repo = BlogRepo()
    try:
        item = await repo.create_blog(data.model_dump())
        return item
    except ClientError as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )

@router.put("/{id}", response_model=BlogDetail)
async def update_blog(id: str, payload: BlogUpdate, admin: dict = Depends(get_current_admin)):
    repo = BlogRepo()
    try:
        updated = await repo.update_blog(id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Blog not found")
        return updated
    except ClientError:
        raise HTTPException(status_code=404, detail="Blog not found")

@router.delete("/{id}")
async def delete_blog(id: str, admin: dict = Depends(get_current_admin)):
    repo = BlogRepo()
    try:
        deleted = await repo.delete_blog(id) 
        if not deleted:
            raise HTTPException(status_code=404, detail="Blog not found")
        return {"message": f"Blog deleted successfully of id {id}"}
    except ClientError:
        raise HTTPException(status_code=404, detail="Blog not found")
    
        