import uuid
from typing import List, Optional

from basic.error.base_error import BusinessError
from basic.minio_client.minio_client import MinioClient
from basic.model.basic_model import EnumOperatorCategory
from basic.utils.rich_text_util import refresh_rich_text_image_url
from basic_module.model.validate_token_model import ValidateTokenResModel
from biz_module.model.wiki_page_model import (
    WikiPageModel,
    EditWikiPageParamsModel,
    DeleteWikiPageParamsModel,
    SetWikiPageVisibilityParamsModel,
    WikiPageTreeItemModel,
    SaveWikiPageTreeParamsModel,
    PublicWikiSearchResultModel,
)
from biz_module.model.wiki_project_model import HOME_WIKI_PROJECT_CODE
from biz_module.repository.wiki_page_repository import WikiPageRepository
from biz_module.repository.wiki_project_repository import WikiProjectRepository


class WikiPageService:
    def __init__(
            self,
            wiki_page_repository: WikiPageRepository,
            wiki_project_repository: WikiProjectRepository,
            minio_client: MinioClient,
    ):
        self.__wiki_page_repository = wiki_page_repository
        self.__wiki_project_repository = wiki_project_repository
        self.__minio_client = minio_client

    def __get_home_project_id(self) -> Optional[str]:
        project = self.__wiki_project_repository.get_by_code(code=HOME_WIKI_PROJECT_CODE)
        if not project:
            return None
        return project.id

    def __is_home_project(self, project_id: str) -> bool:
        home_project_id = self.__get_home_project_id()
        return home_project_id == project_id

    def get_tree(self, project_id: str) -> List[WikiPageTreeItemModel]:
        flat_list = self.__wiki_page_repository.get_flat_list(
            project_id=project_id,
            include_empty_project=self.__is_home_project(project_id=project_id),
        )
        return self.__build_tree(flat_list=flat_list, parent_id=None)

    def get_public_tree(self, project_id: str) -> List[WikiPageTreeItemModel]:
        flat_list = self.__wiki_page_repository.get_public_flat_list(
            project_id=project_id,
            include_empty_project=self.__is_home_project(project_id=project_id),
        )
        return self.__build_tree(flat_list=flat_list, parent_id=None)

    def search_public_list(self, search: str, page: int, page_size: int) -> PublicWikiSearchResultModel:
        if not search or not search.strip():
            return PublicWikiSearchResultModel()
        page = max(1, page or 1)
        page_size = max(1, min(page_size or 20, 50))
        data_list = self.__wiki_page_repository.search_public_list(
            search=search.strip(),
            page=page,
            page_size=page_size,
            fetch_size=page_size + 1,
        )
        return PublicWikiSearchResultModel(
            data_list=data_list[:page_size],
            has_more=len(data_list) > page_size,
        )

    def __build_tree(self, flat_list: List[WikiPageTreeItemModel], parent_id) -> List[WikiPageTreeItemModel]:
        result = []
        for page in flat_list:
            if page.parent_id == parent_id:
                item = WikiPageTreeItemModel(
                    id=page.id,
                    project_id=page.project_id,
                    title=page.title,
                    seq=page.seq,
                    parent_id=page.parent_id,
                    is_public=page.is_public,
                    require_auth=page.require_auth,
                    access_code=page.access_code,
                    child_list=self.__build_tree(flat_list=flat_list, parent_id=page.id)
                )
                result.append(item)
        return result

    def get_detail(self, page_id: str) -> WikiPageModel:
        page = self.__wiki_page_repository.get_by_id(page_id=page_id)
        if not page:
            raise BusinessError('页面不存在')
        page.content = refresh_rich_text_image_url(
            content=page.content,
            minio_client=self.__minio_client,
        )
        return page

    def get_public_detail(self, page_id: str, auth_code: str = None, project_id: str = None) -> WikiPageModel:
        page = self.__wiki_page_repository.get_public_detail(page_id=page_id)
        if not page:
            raise BusinessError('页面不存在或未公开')
        if project_id and page.project_id != project_id:
            if not (self.__is_home_project(project_id=project_id) and page.project_id is None):
                raise BusinessError('页面不存在或未公开')
        if page.require_auth and page.access_code != auth_code:
            raise BusinessError('需要授权码才能查看')
        page.content = refresh_rich_text_image_url(
            content=page.content,
            minio_client=self.__minio_client,
        )
        page.access_code = None
        return page

    def edit(
            self,
            params: EditWikiPageParamsModel,
            current_user_info: ValidateTokenResModel
    ):
        if params.page_id:
            exist = self.__wiki_page_repository.get_by_id(page_id=params.page_id)
            if not exist:
                raise BusinessError('页面不存在')
            dup = self.__wiki_page_repository.get_exist(
                project_id=params.project_id,
                title=params.title,
                page_id=params.page_id,
                include_empty_project=self.__is_home_project(project_id=params.project_id),
            )
            if dup:
                raise BusinessError('页面标题已存在')
            exist.title = params.title
            exist.project_id = params.project_id
            exist.content = params.content
            exist.parent_id = params.parent_id
            exist.seq = params.seq
            exist.is_public = params.is_public
            exist.require_auth = params.require_auth if params.is_public else False
            if exist.require_auth and not params.access_code and not exist.access_code:
                raise BusinessError('授权码不能为空')
            exist.access_code = (params.access_code or exist.access_code) if exist.require_auth else None
            exist.operator_category = EnumOperatorCategory.UNION_USER.value
            exist.operator = current_user_info.union_user_info.id
            self.__wiki_page_repository.update(model=exist)
            return exist.id

        dup = self.__wiki_page_repository.get_exist(
            project_id=params.project_id,
            title=params.title,
            include_empty_project=self.__is_home_project(project_id=params.project_id),
        )
        if dup:
            raise BusinessError('页面标题已存在')
        require_auth = params.require_auth if params.is_public else False
        if require_auth and not params.access_code:
            raise BusinessError('授权码不能为空')
        new_id = str(uuid.uuid4())
        model = WikiPageModel(
            id=new_id,
            creator=current_user_info.union_user_info.id,
            project_id=params.project_id,
            parent_id=params.parent_id,
            title=params.title,
            content=params.content,
            seq=params.seq,
            is_public=params.is_public,
            require_auth=require_auth,
            access_code=params.access_code if require_auth else None,
            is_deleted=False,
            operator_category=EnumOperatorCategory.UNION_USER.value,
            operator=current_user_info.union_user_info.id,
        )
        self.__wiki_page_repository.insert(model=model)
        return new_id

    def set_visibility(self, params: SetWikiPageVisibilityParamsModel):
        exist = self.__wiki_page_repository.get_by_id(page_id=params.page_id)
        if not exist:
            raise BusinessError('页面不存在')
        exist.is_public = params.is_public
        exist.require_auth = params.require_auth if params.is_public else False
        if exist.require_auth and not params.access_code and not exist.access_code:
            raise BusinessError('授权码不能为空')
        exist.access_code = (params.access_code or exist.access_code) if exist.require_auth else None
        self.__wiki_page_repository.update(model=exist)

    def delete(self, params: DeleteWikiPageParamsModel):
        exist = self.__wiki_page_repository.get_by_id(page_id=params.page_id)
        if not exist:
            raise BusinessError('页面不存在')
        page_id_list = [params.page_id]
        page_id_list.extend(
            self.__wiki_page_repository.get_all_descendant_id_list(page_id=params.page_id)
        )
        for page_id in page_id_list:
            page = self.__wiki_page_repository.get_by_id(page_id=page_id)
            if page:
                page.is_deleted = True
                self.__wiki_page_repository.update(model=page)

    def save_tree(self, params: SaveWikiPageTreeParamsModel):
        self.__save_tree_page_list(page_list=params.page_list, parent_id=None)

    def __save_tree_page_list(self, page_list: List[WikiPageTreeItemModel], parent_id):
        for index, page in enumerate(page_list):
            exist = self.__wiki_page_repository.get_by_id(page_id=page.id)
            if exist:
                exist.parent_id = parent_id
                exist.seq = index + 1
                self.__wiki_page_repository.update(model=exist)
            if page.child_list:
                self.__save_tree_page_list(page_list=page.child_list, parent_id=page.id)
