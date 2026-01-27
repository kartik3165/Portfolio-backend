from fastapi import APIRouter
from app.schemas.skill import SkillsResponse, SkillAdd, SkillRemove
from app.repositories.skills_repo import SkillsRepo
from app.core.security import get_current_admin
from fastapi import Depends

router = APIRouter(prefix="/skill", tags=["Skills"])

@router.post("/add", response_model=SkillsResponse)
def add_skill(payload: SkillAdd, admin: dict = Depends(get_current_admin)):
    repo = SkillsRepo()
    return repo.add_skill(payload.skill)


@router.post("/remove", response_model=SkillsResponse)
def remove_skill(payload: SkillRemove, admin: dict = Depends(get_current_admin)):
    repo = SkillsRepo()
    return repo.remove_skill(payload.skill)