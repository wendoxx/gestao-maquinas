from __future__ import annotations

from dataclasses import fields
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.domain.entities import Asset
from app.domain.repositories import AssetFilter, AssetRepository
from app.infrastructure.models import AssetModel

_AUTO_FIELDS = {"id", "created_at", "updated_at"}


def _to_columns(asset: Asset) -> dict:
    return {f.name: getattr(asset, f.name) for f in fields(asset) if f.name not in _AUTO_FIELDS}


def _to_entity(m: AssetModel) -> Asset:
    return Asset(**{f.name: getattr(m, f.name) for f in fields(Asset)})


class SqlAssetRepository(AssetRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, asset: Asset) -> Asset:
        model = AssetModel(**_to_columns(asset))
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return _to_entity(model)

    def get_by_id(self, asset_id: int) -> Optional[Asset]:
        m = self.session.get(AssetModel, asset_id)
        return _to_entity(m) if m else None

    def get_by_code(self, code: str) -> Optional[Asset]:
        m = self.session.scalar(select(AssetModel).where(AssetModel.code == code))
        return _to_entity(m) if m else None

    def list(self, filter_: AssetFilter) -> tuple[list[Asset], int]:
        conditions = []
        if filter_.q:
            like = f"%{filter_.q}%"
            conditions.append(or_(AssetModel.name.ilike(like), AssetModel.code.ilike(like),
                                  AssetModel.brand.ilike(like), AssetModel.model.ilike(like),
                                  AssetModel.serial_number.ilike(like)))
        if filter_.type:
            conditions.append(AssetModel.type == filter_.type)
        if filter_.status:
            conditions.append(AssetModel.status == filter_.status)
        if filter_.category:
            conditions.append(AssetModel.category.ilike(filter_.category))
        if filter_.location:
            conditions.append(AssetModel.location.ilike(f"%{filter_.location}%"))
        if filter_.owner:
            conditions.append(AssetModel.owner.ilike(f"%{filter_.owner}%"))

        total = self.session.scalar(select(func.count()).select_from(AssetModel).where(*conditions)) or 0
        rows = self.session.scalars(
            select(AssetModel).where(*conditions).order_by(AssetModel.name)
            .offset(filter_.skip).limit(filter_.limit)
        ).all()
        return [_to_entity(r) for r in rows], total

    def list_all(self) -> list[Asset]:
        return [_to_entity(r) for r in self.session.scalars(select(AssetModel)).all()]

    def update(self, asset: Asset) -> Asset:
        model = self.session.get(AssetModel, asset.id)
        for field, value in _to_columns(asset).items():
            setattr(model, field, value)
        self.session.commit()
        self.session.refresh(model)
        return _to_entity(model)

    def remove(self, asset_id: int) -> None:
        model = self.session.get(AssetModel, asset_id)
        if model:
            self.session.delete(model)
            self.session.commit()
