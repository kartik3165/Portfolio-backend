from fastapi import APIRouter
from app.schemas.skill import SkillsResponse, SkillAdd, SkillRemove
from app.repositories.skills_repo import SkillsRepo
from app.core.security import verify_passkey

router = APIRouter(prefix="/skill", tags=["Skills"])

@router.post("/add", response_model=SkillsResponse)
async def add_skill(payload: SkillAdd):
    verify_passkey(payload.passkey)
    repo = SkillsRepo()
    return await repo.add_skill(payload.skill)


@router.post("/remove", response_model=SkillsResponse)
async def remove_skill(payload: SkillRemove):
    verify_passkey(payload.passkey)
    repo = SkillsRepo()
    return await repo.remove_skill(payload.skill)