from sqlalchemy.orm import Session
from models import Player
from w2project.schemas.player import PlayerCreate
def get_player_by_nickname(db: Session, name: str) -> Player:
    return db.query(Player).filter(Player.nickname == name).first()

def get_player(db: Session, id: str) -> Player:
    return db.query(Player).filter(Player.player_id == id).first()

def create_player(db: Session, player: PlayerCreate):
    player_db = Player(
        nickname = player.nickname,
        logo_url = player.logo_url,
        riot_id = player.riot_id,
        ct_slug = player.ct_slug
    )
    db.add(player_db)
    db.commit()
    db.refresh(player_db)
    return player_db

def create_or_get_player(db: Session, player: PlayerCreate):
    db_player = get_player_by_nickname(db, player.nickname)
    if not db_player:
        db_player = create_player(db, player)
    return db_player