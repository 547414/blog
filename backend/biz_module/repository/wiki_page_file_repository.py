from typing import List, Optional

from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from biz_module.entity.wiki_page_file import WikiPageFileEntity
from biz_module.model.wiki_page_file_model import WikiPageFileModel


class WikiPageFileRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: WikiPageFileModel):
        return self.add(
            model=model,
            entity=WikiPageFileEntity
        )

    def update(self, model: WikiPageFileModel):
        return self.update_entity(
            entity=WikiPageFileEntity,
            entity_id=model.id,
            model=model
        )

    def get_by_id(self, file_id: str) -> Optional[WikiPageFileModel]:
        sql = """
        SELECT * FROM bt_wiki_page_file
        WHERE id = :file_id
          AND is_deleted IS FALSE
        """
        return self.get_by_params(
            sql=sql,
            model=WikiPageFileModel,
            params={'file_id': file_id}
        )

    def get_list_by_page_id(self, page_id: str) -> List[WikiPageFileModel]:
        sql = """
        SELECT * FROM bt_wiki_page_file
        WHERE page_id = :page_id
          AND is_deleted IS FALSE
        ORDER BY created_at
        """
        return self.get_all_by_params(
            sql=sql,
            model=WikiPageFileModel,
            params={'page_id': page_id}
        )
