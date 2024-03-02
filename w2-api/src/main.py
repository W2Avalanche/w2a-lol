from fastapi import FastAPI, Depends, HTTPException
from datetime import timedelta

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import Base, engine
from w2project.schemas.auth import User, Token
from w2project.schemas.team import Team
from w2project.schemas.player import Player

from crud.crud_player import create_player, get_player_by_nickname, create_or_get_player
from crud.crud_team import create_team, get_team_by_name, create_or_update_team, get_all_teams
from deps import get_current_active_user, get_db
from auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

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