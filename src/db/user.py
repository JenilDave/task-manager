from src.db.base import Base
from sqlalchemy import String, Column

class User(Base):
    __tablename__ = "user"

    username: str = Column(String(100), nullable=False, unique=True)
    email: str = Column(String(255), nullable=False, unique=True)
    hashed_password: str = Column(String(255), nullable=False)