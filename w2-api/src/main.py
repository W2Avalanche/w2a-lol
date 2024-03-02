from fastapi import FastAPI, Depends, HTTPException
from datetime import timedelta
import websockets

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import Base, engine
from w2project.schemas.auth import User, Token
from w2project.schemas.team import Team
from w2project.schemas.player import Player
from w2project.schemas.game import GameStruct, GameMessage, GameSwapRequest, PickStatusEnum

from crud.crud_player import create_player, get_player_by_nickname, create_or_get_player
from crud.crud_team import create_team, get_team_by_name, create_or_update_team, get_all_teams
from deps import get_current_active_user, get_db
from auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from utils import get_game_json
import requests
from utils import read_config, Configuration
config : Configuration = read_config('../configuration.json')


app = FastAPI(
    title="W2 API",
    version="αlpha 0.1"
)
@app.on_event("startup")
async def setup():
    Base.metadata.create_all(engine)

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db) 
):
    user: User = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
async def get_my_data(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.post("/team")
async def add_team(team: Team,
                   current_user: Annotated[User, Depends(get_current_active_user)],
                   db: Session = Depends(get_db) ):
    players = [ create_or_get_player(db, player) for player in team.players ]
    team = create_or_update_team(db, team, players)

    return team

@app.get("/team/{team_name}", response_model= Team)
async def recover_team(team_name: str, 
                       current_user: Annotated[User, Depends(get_current_active_user)],
                    db: Session = Depends(get_db) ) -> Team:
    team = get_team_by_name(db, team_name)
    return team

@app.get("/teams", response_model= list[Team])
async def list_team(current_user: Annotated[User, Depends(get_current_active_user)],
                    db: Session = Depends(get_db) ) -> Team:
    team = get_all_teams(db)
    return team

@app.post("/match")
async def add_team(game: GameStruct,
                   current_user: Annotated[User, Depends(get_current_active_user)],
                   db: Session = Depends(get_db) ):
    
    game = GameMessage.get_init_message_from_schema("website", current_user.user_name, game)
    async with websockets.connect("ws://{}/game".format(config.game_manager)) as websocket:
        await websocket.send(get_game_json(game.model_dump(mode='json')))
    return game

@app.put("/match/{match_id}/swap")
async def swap_positions(match_id: str,  
                         swap: GameSwapRequest,                  
                         current_user: Annotated[User, Depends(get_current_active_user)],
                   db: Session = Depends(get_db) ):
    game_request = requests.get("http://{}/game/{}".format(config.game_manager, match_id))
    if game_request.status_code != 200:
        raise HTTPException(status_code=404, detail="Match {} not found")
    game = GameMessage(**game_request.json())
    if game.status.state != PickStatusEnum.finished:
        raise HTTPException(status_code=400,detail="picks&ban still running")
    
    game.status.swap_champs(swap.team, swap.swap_position_1, swap.swap_position_2)
    async with websockets.connect("ws://{}/game".format(config.game_manager)) as websocket:
        await websocket.send(get_game_json(game.model_dump(mode='json')))
    return game
