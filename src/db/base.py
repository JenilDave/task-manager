from sqlalchemy import func
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),
        server_default=func.now()
    )
    

