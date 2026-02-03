from fastapi import APIRouter, HTTPException, Depends, Header
from app.repositories.profile_repo import ProfileRepo
from app.schemas.profile import (
    Experience, ExperienceCreate, ExperienceUpdate,
    ResearchPaper, ResearchPaperCreate, ResearchPaperUpdate,
    Achievement, AchievementCreate, AchievementUpdate,
    BioUpdate
)
from app.core.security import verify_passkey

router = APIRouter(prefix="", tags=["Profile (Admin)"])

# --- Experience ---
@router.post("/experience", response_model=Experience)
async def create_experience(payload: ExperienceCreate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        return await repo.create_experience(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/experience/{id}", response_model=Experience)
async def update_experience(id: str, payload: ExperienceUpdate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        updated = await repo.update_experience(id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Experience not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.delete("/experience/{id}")
async def delete_experience(id: str, passkey: str = Header(..., alias="x-admin-passkey")): 
    verify_passkey(passkey)
    repo = ProfileRepo()
    try:
        deleted = await repo.delete_experience(id)
        if not deleted:
             raise HTTPException(status_code=404, detail="Experience not found")
        return {"message": "Experience deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# --- Research Papers ---
@router.post("/research_papers", response_model=ResearchPaper)
async def create_paper(payload: ResearchPaperCreate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        return await repo.create_paper(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/research_papers/{id}", response_model=ResearchPaper)
async def update_paper(id: str, payload: ResearchPaperUpdate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        updated = await repo.update_paper(id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Research Paper not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.delete("/research_papers/{id}")
async def delete_paper(id: str, passkey: str = Header(..., alias="x-admin-passkey")):
    verify_passkey(passkey)
    repo = ProfileRepo()
    try:
        deleted = await repo.delete_paper(id)
        if not deleted:
             raise HTTPException(status_code=404, detail="Research Paper not found")
        return {"message": "Research Paper deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# --- Achievements ---
@router.post("/achievements", response_model=Achievement)
async def create_achievement(payload: AchievementCreate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        return await repo.create_achievement(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/achievements/{id}", response_model=Achievement)
async def update_achievement(id: str, payload: AchievementUpdate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        updated = await repo.update_achievement(id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Achievement not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.delete("/achievements/{id}")
async def delete_achievement(id: str, passkey: str = Header(..., alias="x-admin-passkey")):
    verify_passkey(passkey)
    repo = ProfileRepo()
    try:
        deleted = await repo.delete_achievement(id)
        if not deleted:
             raise HTTPException(status_code=404, detail="Achievement not found")
        return {"message": "Achievement deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.put("/bio")
async def update_bio(payload: BioUpdate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        data = payload.model_dump()
        data.pop("passkey")
        updated = await repo.update_bio(data)
        if not updated:
            raise HTTPException(status_code=500, detail="Failed to update bio")
        return {
            "status": "success",
            "data": {
                "message": "Bio updated successfully"
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
