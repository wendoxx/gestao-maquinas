from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional

from app.domain.exceptions import ValidationError


class AssetType(str, Enum):
    machine = "maquina"
    property = "patrimonio"


class AssetStatus(str, Enum):
    active = "ativo"
    under_maintenance = "em_manutencao"
    inactive = "inativo"
    decommissioned = "baixado"


class MaintenanceType(str, Enum):
    preventive = "preventiva"
    corrective = "corretiva"


@dataclass
class Asset:
    code: str
    name: str
    type: AssetType
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    acquisition_value: Optional[float] = None
    acquisition_date: Optional[date] = None
    useful_life_years: Optional[int] = None
    status: AssetStatus = AssetStatus.active
    notes: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.code or not self.code.strip():
            raise ValidationError("O código do ativo é obrigatório")
        if not self.name or not self.name.strip():
            raise ValidationError("O nome do ativo é obrigatório")
        if self.acquisition_value is not None and self.acquisition_value < 0:
            raise ValidationError("O valor de aquisição não pode ser negativo")
        if self.useful_life_years is not None and self.useful_life_years <= 0:
            raise ValidationError("A vida útil deve ser maior que zero")
        if self.acquisition_date and self.acquisition_date > date.today():
            raise ValidationError("A data de aquisição não pode ser futura")

    def current_value(self, today: Optional[date] = None) -> Optional[float]:
        """Simple straight-line depreciation."""
        if not (self.acquisition_value and self.acquisition_date and self.useful_life_years):
            return self.acquisition_value
        today = today or date.today()
        years_elapsed = (today - self.acquisition_date).days / 365.25
        return round(max(self.acquisition_value * (1 - years_elapsed / self.useful_life_years), 0), 2)


@dataclass
class Maintenance:
    asset_id: int
    date: date
    type: MaintenanceType
    description: str
    cost: Optional[float] = None
    technician: Optional[str] = None
    next_maintenance: Optional[date] = None
    id: Optional[int] = None

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValidationError("A descrição da manutenção é obrigatória")
        if self.cost is not None and self.cost < 0:
            raise ValidationError("O custo não pode ser negativo")
        if self.next_maintenance and self.next_maintenance < self.date:
            raise ValidationError("A próxima manutenção não pode ser anterior à data atual da manutenção")