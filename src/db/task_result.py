from src.db.base import Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class TaskResult(Base):

    __tablename__ = "task_result"

    task_id: Mapped[int] = mapped_column(ForeignKey("task_status.id"), nullable=False)
    status: str = Column(String(255), nullable=False)
    message: str = Column(String(500), nullable=True)
