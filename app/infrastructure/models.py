from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import Date, DateTime, Enum as SAEnum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities import AssetStatus, AssetType, MaintenanceType
from app.infrastructure.database import Base


def _now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _enum(e):
    # Stored as VARCHAR instead of a native Postgres ENUM: simpler migrations.
    return SAEnum(e, native_enum=False, length=30, values_callable=lambda x: [i.value for i in x])


class AssetModel(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    type: Mapped[AssetType] = mapped_column(_enum(AssetType), index=True)
    category: Mapped[Optional[str]] = mapped_column(String(80), index=True)
    brand: Mapped[Optional[str]] = mapped_column(String(80))
    model: Mapped[Optional[str]] = mapped_column(String(80))
    serial_number: Mapped[Optional[str]] = mapped_column(String(80))
    location: Mapped[Optional[str]] = mapped_column(String(120))
    owner: Mapped[Optional[str]] = mapped_column(String(120))
    acquisition_value: Mapped[Optional[float]] = mapped_column(Float)
    acquisition_date: Mapped[Optional[date]] = mapped_column(Date)
    useful_life_years: Mapped[Optional[int]]
    status: Mapped[AssetStatus] = mapped_column(_enum(AssetStatus), default=AssetStatus.active, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now_utc, onupdate=_now_utc)

    maintenances: Mapped[list["MaintenanceModel"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )


class MaintenanceModel(Base):
    __tablename__ = "maintenances"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date)
    type: Mapped[MaintenanceType] = mapped_column(_enum(MaintenanceType))
    description: Mapped[str] = mapped_column(Text)
    cost: Mapped[Optional[float]] = mapped_column(Float)
    technician: Mapped[Optional[str]] = mapped_column(String(120))
    next_maintenance: Mapped[Optional[date]] = mapped_column(Date, index=True)

    asset: Mapped[AssetModel] = relationship(back_populates="maintenances")
