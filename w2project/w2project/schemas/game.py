from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum, IntEnum

class PickPhasesEnum(IntEnum):
    ban_blue_1 = 0
    ban_red_1 = 1
    ban_blue_2 = 2
    ban_red_2 = 3
    ban_blue_3 = 4
    ban_red_3 = 5
    pick_blue_1 = 6
    pick_red_1 = 7
    pick_red_2 = 8
    pick_blue_2 = 9
    pick_blue_3 = 10
    pick_red_3 = 11
    ban_red_4 = 12
    ban_blue_4 = 13
    ban_red_5 = 14
    ban_blue_5 = 15
    pick_red_4 = 16
    pick_blue_4 = 17
    pick_blue_5 = 18
    pick_red_5 = 19
    ended = 20

    def is_blue_turn(self):
        return self in {PickPhasesEnum.ban_blue_1, PickPhasesEnum.ban_blue_2, PickPhasesEnum.ban_blue_3, PickPhasesEnum.ban_blue_4, PickPhasesEnum.ban_blue_5, PickPhasesEnum.pick_blue_1, PickPhasesEnum.pick_blue_2, PickPhasesEnum.pick_blue_3, PickPhasesEnum.pick_blue_4, PickPhasesEnum.pick_blue_5}

    def is_red_turn(self):
        return self in {PickPhasesEnum.ban_red_1, PickPhasesEnum.ban_red_2, PickPhasesEnum.ban_red_3, PickPhasesEnum.ban_red_4, PickPhasesEnum.ban_red_5, PickPhasesEnum.pick_red_1, PickPhasesEnum.pick_red_2, PickPhasesEnum.pick_red_3, PickPhasesEnum.pick_red_4, PickPhasesEnum.pick_red_5}

class GameTeam(BaseModel):
    picks: list[str]
    bans: list[str]
    active: bool

class GameStatus(BaseModel):
    blue_team : GameTeam
    red_team : GameTeam
    phase: PickPhasesEnum
    timer : int

class GameConfig(BaseModel):
    blue_team_name: str
    blue_team_logo: str
    blue_team_players: list[str]
    red_team_name: str
    red_team_logo: str
    red_team_players: list[str]
    tournament_name: str
    tournament_logo: str
    dawe_id: Optional[str]

class GameMessage(BaseModel):
    origin: str
    type: str
    user: str
    status: Optional[GameStatus]
    config: Optional[GameConfig]
    dawe_id: Optional[str]

class ViewTeamConfig(BaseModel):
    name: str
    score : int
    coach : str
    logo: str
    color: str

class ViewGameConfig(BaseModel):
    logo: str 
    scoreEnabled: bool 
    spellsEnabled: bool 
    coachesEnabled: bool 
    blueTeam: ViewTeamConfig
    redTeam: ViewTeamConfig 
    patch: str

class ViewChampion(BaseModel):
    name: str
    idName: str
    loadingImg: str
    squareImg: str

class ViewSelect(BaseModel):
    champion: ViewChampion
    isActive: bool
    displayName: Optional[str]

class ViewTeamState(BaseModel): 
    picks: list[ViewSelect]
    bans: list[ViewSelect]
    isActive: bool

class ViewGameState(BaseModel): 
    config: ViewGameConfig 
    blueTeam : ViewTeamState
    redTeam : ViewTeamState 
    timer: int
    champSelectActive: bool
    leagueConnected: bool
class ViewGame(BaseModel):
    eventType: str 
    state: ViewGameState