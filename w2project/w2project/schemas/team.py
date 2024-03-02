from pydantic import BaseModel, Field
from .player import Player
from typing import Optional

import uuid
class TeamBase(BaseModel):
    team_id: Optional[uuid.UUID] = Field(default=None)
    name: str
    logo_url: Optional[str]
    players: list[Player]
    ct_slug: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    class Config:
        from_attrobites = True