from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey
)
from core.database import Base


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    tasks = relationship("TaskModel", back_populates="user")
    
    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, is_active={self.is_active})"


class Tokenmodel(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String(), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    
    user = relationship("UserModel", uselist=False)
    