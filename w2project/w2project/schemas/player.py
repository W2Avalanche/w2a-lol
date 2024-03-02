from pydantic import BaseModel, Field
from typing import Optional

import uuid
class PlayerBase(BaseModel):
    player_id: Optional[uuid.UUID] = Field(default=None)
    nickname: str
    riot_id: Optional[str] = Field(default=None, )
    lol_nickname: Optional[str] = Field(default=None)
    logo_url: Optional[str] = Field(default=None)
    ct_slug: Optional[str]
    
class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    class Config:
        from_attrobites = True