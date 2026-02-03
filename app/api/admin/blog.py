from fastapi import APIRouter, HTTPException, Depends
from botocore.exceptions import ClientError
from typing import List

from app.schemas.blog import BlogCreate, BlogDelete, BlogDetailAdmin, BlogUpdate
from app.repositories.blog_repo import BlogRepo
from app.core.security import verify_passkey

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.get("", response_model=List[BlogDetailAdmin])
async def list_all_blogs(passkey: str):
    verify_passkey(passkey)
    repo = BlogRepo()
    try:
        data = await repo.list_blogs(include_drafts=True)
        return data
    except ClientError:
        raise HTTPException(
            status_code=404, 
            detail="Unable to fetch Blogs"
        )


@router.post("", response_model=BlogDetailAdmin)
async def create_blog(data: BlogCreate):
    verify_passkey(data.passkey)
    repo = BlogRepo()
    try:
        item = await repo.create_blog(data.model_dump())
        return item
    except ClientError as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )

@router.put("/{id}", response_model=BlogDetailAdmin)
async def update_blog(id: str, payload: BlogUpdate):
    verify_passkey(payload.passkey)
    repo = BlogRepo()
    try:
        updated = await repo.update_blog(id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Blog not found")
        return updated
    except ClientError:
        raise HTTPException(status_code=404, detail="Blog not found")

@router.delete("/{id}")
async def delete_blog(id: str, payload: BlogDelete):
    verify_passkey(payload.passkey)
    repo = BlogRepo()
    try:
        deleted = await repo.delete_blog(id) 
        if not deleted:
            raise HTTPException(status_code=404, detail="Blog not found")
        return {"message": f"Blog deleted successfully of id {id}"}
    except ClientError:
        raise HTTPException(status_code=404, detail="Blog not found")
    
        