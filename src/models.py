from sqlalchemy import DeclarativeBase, mapped_column, Mapped, func, DateTime
from datetime import datetime
from typing import Optional

class Base(DeclarativeBase):
    pass

class HistorySearchModel(Base):
    __tablename__ = "searches"

    # id: Llave Primaria (PK) autoincremental
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    #coordinates and parameters
    address_query: Mapped[Optional[str]] = mapped_column(nullable=True) # Dirección ingresada si la hubo
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    radius_km: Mapped[float] = mapped_column(nullable=False)
    
    #Wikipedia data
    place_title: Mapped[str] = mapped_column(nullable=False)
    distance_km: Mapped[float] = mapped_column(nullable=False)
    page_url: Mapped[str] = mapped_column(nullable=False)
    
    #timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
    server_default=func.now(),
    nullable=False)