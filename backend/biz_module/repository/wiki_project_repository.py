from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from basic.model.pagination_model import Pagination
from basic.repository.base_repository import BaseRepository
from biz_module.entity.wiki_project import WikiProjectEntity
from biz_module.model.wiki_project_model import WikiProjectModel, PublicWikiProjectItemModel


class WikiProjectRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: WikiProjectModel):
        return self.add(
            model=model,
            entity=WikiProjectEntity
        )

    def update(self, model: WikiProjectModel):
        return self.update_entity(
            entity=WikiProjectEntity,
            entity_id=model.id,
            model=model
        )

    def get_by_id(self, project_id: str) -> Optional[WikiProjectModel]:
        sql = """
        SELECT * FROM bt_wiki_project
        WHERE id = :project_id
          AND is_deleted IS FALSE
        """
        return self.get_by_params(
            sql=sql,
            model=WikiProjectModel,
            params={'project_id': project_id}
        )

    def get_by_code(self, code: str) -> Optional[WikiProjectModel]:
        sql = """
        SELECT * FROM bt_wiki_project
        WHERE code = :code
          AND is_deleted IS FALSE
        """
        return self.get_by_params(
            sql=sql,
            model=WikiProjectModel,
            params={'code': code}
        )

    def get_list(self) -> List[WikiProjectModel]:
        sql = """
        SELECT * FROM bt_wiki_project
        WHERE is_deleted IS FALSE
          AND code != 'HOME_PROJECT'
        ORDER BY seq, created_at
        """
        return self.get_all_by_params(
            sql=sql,
            model=WikiProjectModel,
            params={}
        )

    def page(
            self,
            page_index: int,
            page_size: int,
            search: Optional[str] = None,
    ) -> Pagination:
        sql = """
        SELECT * FROM bt_wiki_project
        WHERE is_deleted IS FALSE
          AND code != 'HOME_PROJECT'
        """
        params: Dict[str, Any] = {'search': None}
        if search:
            sql += """
            AND (
              code LIKE :search
              OR name LIKE :search
            )
            """
            params['search'] = f'%{search}%'
        sql += """
        ORDER BY seq, created_at
        """
        return self.get_page(
            sql=sql,
            data_model=WikiProjectModel,
            page_index=page_index,
            page_size=page_size,
            search=None,
            search_fields=None,
            params=params,
        )

    def get_public_page(
            self,
            page_index: int,
            page_size: int,
            search: Optional[str] = None,
    ) -> Pagination:
        sql = """
        SELECT
            wp.*,
            sub.wiki_count,
            sub.latest_updated_at
        FROM bt_wiki_project wp
        INNER JOIN (
            SELECT
                p.project_id,
                COUNT(p.id) AS wiki_count,
                MAX(COALESCE(p.updated_at, p.created_at)) AS latest_updated_at
            FROM bt_wiki_page p
            WHERE p.is_public IS TRUE
              AND p.is_deleted IS FALSE
            GROUP BY p.project_id
        ) sub ON sub.project_id = wp.id
        WHERE wp.is_deleted IS FALSE
          AND wp.code != 'HOME_PROJECT'
        """
        params: Dict[str, Any] = {'search': None}
        if search and search.strip():
            sql += """
            AND (
              wp.code LIKE :search
              OR wp.name LIKE :search
              OR wp."desc" LIKE :search
              OR EXISTS (
                SELECT 1 FROM bt_wiki_page p2
                WHERE p2.project_id = wp.id
                  AND p2.is_public IS TRUE
                  AND p2.is_deleted IS FALSE
                  AND (
                    p2.title LIKE :search
                    OR (p2.require_auth IS FALSE AND p2.content LIKE :search)
                  )
              )
            )
            """
            params['search'] = f'%{search.strip()}%'
        sql += """
        ORDER BY wp.seq, sub.latest_updated_at DESC NULLS LAST, wp.created_at DESC
        """
        return self.get_page(
            sql=sql,
            data_model=PublicWikiProjectItemModel,
            page_index=page_index,
            page_size=page_size,
            search=None,
            search_fields=None,
            params=params,
        )

    def get_exist(self, code: str, project_id: Optional[str] = None) -> Optional[WikiProjectModel]:
        sql = """
        SELECT * FROM bt_wiki_project
        WHERE code = :code
          AND is_deleted IS FALSE
        """
        if project_id:
            sql += """
            AND id != :project_id
            """
        return self.get_by_params(
            sql=sql,
            model=WikiProjectModel,
            params={'code': code, 'project_id': project_id}
        )
