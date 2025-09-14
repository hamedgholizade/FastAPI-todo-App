from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from core.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(
        DateTime(), default=datetime.now, onupdate=datetime.now
    )
    user = relationship("UserModel", back_populates="tasks", uselist=False)

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, \
                is_completed={self.is_completed})"
