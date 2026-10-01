from dataclasses import fields
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.entities import Maintenance
from app.domain.repositories import MaintenanceRepository
from app.infrastructure.models import MaintenanceModel


def _to_entity(m: MaintenanceModel) -> Maintenance:
    return Maintenance(**{f.name: getattr(m, f.name) for f in fields(Maintenance)})


class SqlMaintenanceRepository(MaintenanceRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, maintenance: Maintenance) -> Maintenance:
        model = MaintenanceModel(**{f.name: getattr(maintenance, f.name)
                                    for f in fields(maintenance) if f.name != "id"})
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return _to_entity(model)

    def list_by_asset(self, asset_id: int) -> list[Maintenance]:
        rows = self.session.scalars(
            select(MaintenanceModel).where(MaintenanceModel.asset_id == asset_id)
            .order_by(MaintenanceModel.date.desc())
        ).all()
        return [_to_entity(r) for r in rows]

    def list_pending(self, until: date) -> list[Maintenance]:
        rows = self.session.scalars(
            select(MaintenanceModel)
            .where(MaintenanceModel.next_maintenance.is_not(None), MaintenanceModel.next_maintenance <= until)
            .order_by(MaintenanceModel.next_maintenance)
        ).all()
        return [_to_entity(r) for r in rows]

    def total_cost(self) -> float:
        return float(self.session.scalar(select(func.coalesce(func.sum(MaintenanceModel.cost), 0))) or 0)
