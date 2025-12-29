from src.db.base import Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class TaskStatusHistory(Base):

    __tablename__ = "task_status_history"

    task_id: Mapped[int] = mapped_column(ForeignKey("task_status.id"), nullable=False)
    from_state: str = Column(String(255), nullable=False)
    to_state: str = Column(String(255), nullable=False)