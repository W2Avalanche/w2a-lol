from pydantic import BaseModel, validator

class Status(BaseModel):
    blueName: str
    redName: str
    disabledTurns: list[str]
    disabledChamps: list[str]
    timePerPick: int
    timePerBan: int
    bluePicks: list[str]
    redPicks: list[str]
    blueBans: list[str]
    redBans: list[str]
    nextTeam: str
    nextType: str
    nextTimeout: int
    blueReady: bool
    redReady: bool
    state: str
    turn: int

    @validator('bluePicks', 'redPicks', 'blueBans', 'redBans', pre=True, always=True)
    def cast_elements_to_str(cls, value):
        # If value is not a list, return it as-is
        if not isinstance(value, list):
            return value

        # Convert any integers in the list to strings
        return [str(item) for item in value]
