from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB

from models import Base


class Game(Base):
    __tablename__ = 'game'

    game_id = Column('game_id', Integer, primary_key=True,  nullable=False, autoincrement=False)
    user_id = Column('user_id', Integer, ForeignKey('user.user_id'), primary_key=True, autoincrement=False)
    game_name = Column('game_name', String, nullable=False)
    resources = Column('resources', JSONB)
    army = Column('army', JSONB)
    houses = Column('house', JSONB)
