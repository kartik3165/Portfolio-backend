from fastapi import APIRouter, HTTPException, Depends
from app.repositories.comment_repo import CommentRepo
from app.core.security import verify_passkey

router = APIRouter(prefix="/comment", tags=["Comments (Admin)"])

@router.delete("/{blogId}/{commentId}")
def delete_comment(blogId: str, commentId: str, passkey: str):
    verify_passkey(passkey)
    repo = CommentRepo()
    deleted = repo.delete_comment(blogId, commentId)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
