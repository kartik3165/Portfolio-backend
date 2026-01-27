from fastapi import APIRouter, HTTPException
from app.repositories.profile_repo import ProfileRepo
from app.schemas.profile import (
    ExperienceResponse,
    ResearchPaperResponse,
    AchievementResponse
)

router = APIRouter(prefix="", tags=["Profile"])

@router.get("/experience", response_model=ExperienceResponse)
def get_experience():
    repo = ProfileRepo()
    items = repo.list_experience()
    return {"experience": items}

@router.get("/research_papers", response_model=ResearchPaperResponse)
def get_research_papers():
    repo = ProfileRepo()
    items = repo.list_papers()
    return {"research_papers": items}

@router.get("/achievements", response_model=AchievementResponse)
def get_achievements():
    repo = ProfileRepo()
    items = repo.list_achievements()
    return {"achievements": items}
