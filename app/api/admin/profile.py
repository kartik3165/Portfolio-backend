from fastapi import APIRouter, HTTPException, Depends
from app.repositories.profile_repo import ProfileRepo
from app.schemas.profile import (
    Experience, ExperienceCreate, ExperienceUpdate,
    ResearchPaper, ResearchPaperCreate, ResearchPaperUpdate,
    Achievement, AchievementCreate, AchievementUpdate
)
from app.repositories.profile_repo import ProfileRepo
from app.core.security import verify_passkey

router = APIRouter(prefix="", tags=["Profile (Admin)"])

# --- Experience ---
@router.post("/experience", response_model=Experience)
def create_experience(payload: ExperienceCreate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        return repo.create_experience(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/experience/{id}", response_model=Experience)
def update_experience(id: str, payload: ExperienceUpdate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        updated = repo.update_experience(id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Experience not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.delete("/experience/{id}")
def delete_experience(id: str, passkey: str): 
    verify_passkey(passkey)
    repo = ProfileRepo()
    try:
        deleted = repo.delete_experience(id)
        if not deleted:
             raise HTTPException(status_code=404, detail="Experience not found")
        return {"message": "Experience deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# --- Research Papers ---
@router.post("/research_papers", response_model=ResearchPaper)
def create_paper(payload: ResearchPaperCreate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        return repo.create_paper(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/research_papers/{id}", response_model=ResearchPaper)
def update_paper(id: str, payload: ResearchPaperUpdate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        updated = repo.update_paper(id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Research Paper not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.delete("/research_papers/{id}")
def delete_paper(id: str, passkey: str):
    verify_passkey(passkey)
    repo = ProfileRepo()
    try:
        deleted = repo.delete_paper(id)
        if not deleted:
             raise HTTPException(status_code=404, detail="Research Paper not found")
        return {"message": "Research Paper deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

# --- Achievements ---
@router.post("/achievements", response_model=Achievement)
def create_achievement(payload: AchievementCreate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        return repo.create_achievement(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/achievements/{id}", response_model=Achievement)
def update_achievement(id: str, payload: AchievementUpdate):
    verify_passkey(payload.passkey)
    repo = ProfileRepo()
    try:
        updated = repo.update_achievement(id, payload.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Achievement not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.delete("/achievements/{id}")
def delete_achievement(id: str, passkey: str):
    verify_passkey(passkey)
    repo = ProfileRepo()
    try:
        deleted = repo.delete_achievement(id)
        if not deleted:
             raise HTTPException(status_code=404, detail="Achievement not found")
        return {"message": "Achievement deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
