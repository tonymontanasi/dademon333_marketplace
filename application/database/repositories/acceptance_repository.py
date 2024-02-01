from application.database.models.acceptance import Acceptance, UpdateAcceptance
from application.database.orm_models import AcceptanceORM
from application.database.repositories.base_repository import BaseDbRepository


class AcceptanceRepository(BaseDbRepository[Acceptance, UpdateAcceptance, AcceptanceORM]):
    _model = Acceptance
    _table = AcceptanceORM
