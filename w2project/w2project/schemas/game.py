from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum, IntEnum, StrEnum
from .team import TeamStruct
class PickStatusEnum(StrEnum):
    wating = "waiting"
    on_going = "ongoing"
    finished = "finished"

class PositionsEnum(IntEnum):
    top = 0
    jungler = 1
    mid = 2
    adc = 3
    support = 4

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
    def swap_champs(self, position_1: PositionsEnum, position_2: PositionsEnum):
        _buffer = self.picks[position_1]
        self.picks[position_1] = self.picks[position_2]
        self.picks[position_2] = _buffer

class GameStatus(BaseModel):
    blue_team : GameTeam
    red_team : GameTeam
    phase: PickPhasesEnum
    state: PickStatusEnum
    timer : int
    def swap_champs(self, team:str, position_1: PositionsEnum, position_2: PositionsEnum):
        if team=="blue":
            self.blue_team.swap_champs(position_1=position_1, position_2=position_2)
        elif team=="red":
            self.red_team.swap_champs(position_1=position_1, position_2=position_2)
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
class GameStruct(BaseModel):
    dawe_id: str
    blue_team: TeamStruct
    red_team: TeamStruct
    tournament_name: str
    tournament_logo: str
class GameMessage(BaseModel):
    origin: str
    type: str
    user: str
    status: Optional[GameStatus]
    config: Optional[GameConfig]
    dawe_id: Optional[str]

    def get_init_message_from_schema(origin:str, user: str, game: GameStruct):
        return GameMessage(origin=origin, type="CREATE", user=user,
                           status= None, config= GameConfig(
                               blue_team_name=game.blue_team.name, blue_team_logo=game.blue_team.logo_url,
                               blue_team_players=game.blue_team.players,
                               red_team_name=game.red_team.name, red_team_logo=game.red_team.logo_url,
                               red_team_players=game.red_team.players, tournament_name=game.tournament_name, tournament_logo=game.tournament_logo, dawe_id=game.dawe_id),
                               dawe_id=game.dawe_id
        )

class GameSwapRequest(BaseModel):
    team: str
    swap_position_1: PositionsEnum
    swap_position_2: PositionsEnum
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
    anyTeam: bool


class ViewGame(BaseModel):
    eventType: str 
    state: ViewGameState

