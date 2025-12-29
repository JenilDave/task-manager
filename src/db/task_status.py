from src.db.base import Base
from sqlalchemy import String, Column

class TaskStatus(Base):

    __tablename__ = "task_status"

    title: str = Column(String(100), nullable=False)
    description: str = Column(String(255), nullable=False)
    status: str = Column(String(100), nullable=False)