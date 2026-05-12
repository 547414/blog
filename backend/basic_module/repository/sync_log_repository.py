from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from basic_module.entity.sync_log import SyncLogEntity
from basic_module.model.sync_log_model import SyncLogModel


class SyncLogRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: SyncLogModel):
        return self.add(
            model=model,
            entity=SyncLogEntity
        )

    def update(self, model: SyncLogModel):
        return self.update_entity(
            entity=SyncLogEntity,
            entity_id=model.id,
            model=model
        )
