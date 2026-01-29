from pydantic import BaseModel
from typing import List


class SkillsResponse(BaseModel):
    skills: List[str]

class SkillAdd(BaseModel):
    passkey: str
    skill: str

class SkillRemove(BaseModel):
    passkey: str
    skill: str