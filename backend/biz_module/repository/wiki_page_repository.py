from typing import List, Optional

from sqlalchemy.orm import Session

from basic.repository.base_repository import BaseRepository
from biz_module.entity.wiki_page import WikiPageEntity
from biz_module.model.wiki_page_model import WikiPageModel, WikiPageTreeItemModel, PublicWikiSearchItemModel


class WikiPageRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: WikiPageModel):
        return self.add(
            model=model,
            entity=WikiPageEntity
        )

    def update(self, model: WikiPageModel):
        return self.update_entity(
            entity=WikiPageEntity,
            entity_id=model.id,
            model=model
        )

    def get_by_id(self, page_id: str) -> Optional[WikiPageModel]:
        sql = """
        SELECT * FROM bt_wiki_page
        WHERE id = :page_id
          AND is_deleted IS FALSE
        """
        return self.get_by_params(
            sql=sql,
            model=WikiPageModel,
            params={'page_id': page_id}
        )

    def get_flat_list(self, project_id: str, include_empty_project: bool = False) -> List[WikiPageTreeItemModel]:
        sql = """
        SELECT id, project_id, title, seq, parent_id, is_public, require_auth, access_code
        FROM bt_wiki_page
        WHERE is_deleted IS FALSE
          AND (
            project_id = :project_id
            OR (:include_empty_project IS TRUE AND project_id IS NULL)
          )
        ORDER BY seq, created_at
        """
        return self.get_all_by_params(
            sql=sql,
            model=WikiPageTreeItemModel,
            params={'project_id': project_id, 'include_empty_project': include_empty_project}
        )

    def get_public_flat_list(self, project_id: str, include_empty_project: bool = False) -> List[WikiPageTreeItemModel]:
        sql = """
        SELECT id, project_id, title, seq, parent_id, is_public, require_auth
        FROM bt_wiki_page
        WHERE is_public IS TRUE
          AND is_deleted IS FALSE
          AND (
            project_id = :project_id
            OR (:include_empty_project IS TRUE AND project_id IS NULL)
          )
        ORDER BY seq, created_at
        """
        return self.get_all_by_params(
            sql=sql,
            model=WikiPageTreeItemModel,
            params={'project_id': project_id, 'include_empty_project': include_empty_project}
        )

    def get_public_detail(self, page_id: str) -> Optional[WikiPageModel]:
        sql = """
        SELECT * FROM bt_wiki_page
        WHERE id = :page_id
          AND is_public IS TRUE
          AND is_deleted IS FALSE
        """
        return self.get_by_params(
            sql=sql,
            model=WikiPageModel,
            params={'page_id': page_id}
        )

    def get_all_descendant_id_list(self, page_id: str) -> List[str]:
        sql = """
        WITH RECURSIVE descendants AS (
            SELECT * FROM bt_wiki_page
            WHERE parent_id = :page_id
              AND is_deleted IS FALSE
            UNION ALL
            SELECT p.* FROM bt_wiki_page p
            INNER JOIN descendants d ON p.parent_id = d.id
            WHERE p.is_deleted IS FALSE
        )
        SELECT * FROM descendants
        """
        page_list = self.get_all_by_params(
            sql=sql,
            model=WikiPageModel,
            params={'page_id': page_id}
        )
        return [page.id for page in page_list]

    def get_exist(
            self,
            project_id: str,
            title: str,
            page_id: Optional[str] = None,
            include_empty_project: bool = False,
    ) -> Optional[WikiPageModel]:
        sql = """
        SELECT * FROM bt_wiki_page
        WHERE title = :title
          AND is_deleted IS FALSE
          AND (
            project_id = :project_id
            OR (:include_empty_project IS TRUE AND project_id IS NULL)
          )
        """
        if page_id:
            sql += """
            AND id != :page_id
            """
        return self.get_by_params(
            sql=sql,
            model=WikiPageModel,
            params={
                'project_id': project_id,
                'title': title,
                'page_id': page_id,
                'include_empty_project': include_empty_project,
            }
        )

    def search_public_list(
            self,
            search: str,
            page: int,
            page_size: int,
            fetch_size: int,
    ) -> List[PublicWikiSearchItemModel]:
        sql = """
        SELECT
            p.id AS page_id,
            p.title AS page_title,
            wp.id AS project_id,
            wp.name AS project_name,
            wp.code AS project_code,
            p.require_auth
        FROM bt_wiki_page p
        INNER JOIN bt_wiki_project wp
          ON wp.id = p.project_id
         AND wp.is_deleted IS FALSE
         AND wp.code != 'HOME_PROJECT'
        WHERE p.is_public IS TRUE
          AND p.is_deleted IS FALSE
          AND (
            p.title LIKE :search
            OR (p.require_auth IS FALSE AND p.content LIKE :search)
            OR wp.name LIKE :search
            OR wp.code LIKE :search
          )
        ORDER BY wp.created_at, p.seq, p.created_at
        LIMIT :page_size
        OFFSET :offset
        """
        return self.get_all_by_params(
            sql=sql,
            model=PublicWikiSearchItemModel,
            params={
                'search': f'%{search}%',
                'page_size': fetch_size,
                'offset': (page - 1) * page_size,
            }
        )
