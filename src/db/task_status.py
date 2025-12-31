from src.db.base import Base
from sqlalchemy import String, Column, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

class TaskStatus(Base):

    __tablename__ = "task_status"

    title: str = Column(String(100), nullable=False)
    description: str = Column(String(255), nullable=False)
    status: str = Column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, server_default=text("1"))