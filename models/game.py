from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from repository import Base


class Game(Base):
    __tablename__ = 'game'

    game_id = Column('game_id', Integer, primary_key=True,  nullable=False, autoincrement=False)
    user_id = Column('user_id', Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True, autoincrement=False)
    game_name = Column('game_name', String, nullable=False)
    resources = Column('resources', JSONB)
    army = Column('army', JSONB)
    houses = Column('house', JSONB)
    user = relationship(
        'User',
        back_populates='games',
    )
