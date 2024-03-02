from sqlalchemy.orm import Session
from models import Team, Player
from w2project.schemas.team import TeamCreate
def get_team_by_name(db: Session, name: str) -> Team:
    return db.query(Team).filter(Team.name == name).first()

def get_team(db: Session, id: str) -> Team:
    return db.query(Team).filter(Team.team_id == id).first()

def get_all_teams(db: Session) -> list[Team]:
    return db.query(Team).all()

def create_team(db: Session, team: TeamCreate, players: list[Player] = None):
    team_db = Team(
        name = team.name,
        logo_url = team.logo_url,
        players = players,
        ct_slug = team.ct_slug

    )
    db.add(team_db)
    db.commit()
    db.refresh(team_db)
    return team_db

def create_or_update_team(db: Session, team: TeamCreate, players: list[Player] = None):
    team_db = get_team_by_name(db, team.name)
    if team_db:
        team_db.logo_url = team.logo_url
        team_db.ct_slug = team.ct_slug
        team_db.players = players
        db.commit()
    else:
        team_db = create_team(db, team, players)
    return team_db