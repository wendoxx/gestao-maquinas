"""Ports used by the application layer. Implementations live in infrastructure."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.domain.entities import Asset, AssetStatus, AssetType, Maintenance


@dataclass
class AssetFilter:
    q: Optional[str] = None
    type: Optional[AssetType] = None
    status: Optional[AssetStatus] = None
    category: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    skip: int = 0
    limit: int = 20


class AssetRepository(ABC):
    @abstractmethod
    def add(self, asset: Asset) -> Asset: ...

    @abstractmethod
    def get_by_id(self, asset_id: int) -> Optional[Asset]: ...

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Asset]: ...

    @abstractmethod
    def list(self, filter_: AssetFilter) -> tuple[list[Asset], int]: ...

    @abstractmethod
    def list_all(self) -> list[Asset]: ...

    @abstractmethod
    def update(self, asset: Asset) -> Asset: ...

    @abstractmethod
    def remove(self, asset_id: int) -> None: ...
