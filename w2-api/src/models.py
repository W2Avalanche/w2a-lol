from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.orm import relationship

from database import Base
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

class Team(Base):
    __tablename__ = "teams"

    team_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, index=True)
    logo_url = Column(String(1000))
    ct_slug = Column(String(100), nullable=True)
    players = relationship("Player", secondary="members")

class Player(Base):
    __tablename__ = "players"
    
    player_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String(255), unique=True, index=True)
    riot_id = Column(String(255), nullable=True)
    logo_url = Column(String(1000), nullable=True)
    ct_slug = Column(String(100), nullable=True)


class Membership(Base):
    __tablename__ = 'members'

    team_id = Column(UUID(255), ForeignKey('teams.team_id'), primary_key = True)
    player_id = Column(UUID(255), ForeignKey('players.player_id'), primary_key = True)