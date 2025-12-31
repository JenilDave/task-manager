from sqlalchemy import func, MetaData
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base(DeclarativeBase):

    metadata = MetaData(naming_convention=convention)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),
        server_default=func.now()
    )
    

