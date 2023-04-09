from sqlalchemy import (Column, Integer, String, 
                        Boolean, ForeignKey, DateTime)

from models import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'user'

    user_id = Column('user_id', Integer, primary_key=True)
    email = Column('email', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    token = Column('token', String)
    is_registered = Column('is_registered', Boolean, default=False)
    

class UserCode(Base):
    __tablename__ = 'user_code'

    user_id = Column('user_id', Integer, ForeignKey('user.user_id'),  primary_key=True)
    code = Column('code', String, nullable=False)
    created_at = Column('created_at', DateTime, server_default=func.now())