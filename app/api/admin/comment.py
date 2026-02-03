from fastapi import APIRouter, HTTPException, Depends, Header
from app.repositories.comment_repo import CommentRepo
from app.core.security import verify_passkey

router = APIRouter(prefix="/comment", tags=["Comments (Admin)"])

@router.delete("/{blogId}/{commentId}")
async def delete_comment(blogId: str, commentId: str, passkey: str = Header(..., alias="x-admin-passkey")):
    verify_passkey(passkey)
    repo = CommentRepo()
    deleted = await repo.delete_comment(blogId, commentId)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
