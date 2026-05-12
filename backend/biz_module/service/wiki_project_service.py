import uuid

from basic.error.base_error import BusinessError
from basic.model.pagination_model import Pagination
from basic.model.basic_model import EnumOperatorCategory
from basic_module.model.validate_token_model import ValidateTokenResModel
from biz_module.model.wiki_project_model import (
    HOME_WIKI_PROJECT_CODE,
    WikiProjectModel,
    EditWikiProjectParamsModel,
    DeleteWikiProjectParamsModel,
    WikiProjectPageParamsModel,
)
from biz_module.repository.wiki_project_repository import WikiProjectRepository


class WikiProjectService:
    def __init__(
            self,
            wiki_project_repository: WikiProjectRepository,
    ):
        self.__wiki_project_repository = wiki_project_repository

    def ensure_home_project(self) -> WikiProjectModel:
        project = self.__wiki_project_repository.get_by_code(code=HOME_WIKI_PROJECT_CODE)
        if project:
            return project
        model = WikiProjectModel(
            id=str(uuid.uuid4()),
            code=HOME_WIKI_PROJECT_CODE,
            name='首页',
            is_deleted=False,
            operator_category=EnumOperatorCategory.ROBOT.value,
            operator='system',
        )
        self.__wiki_project_repository.insert(model=model)
        return model

    def get_by_id(self, project_id: str) -> WikiProjectModel:
        project = self.__wiki_project_repository.get_by_id(project_id=project_id)
        if not project:
            raise BusinessError('项目不存在')
        return project

    def get_list(self):
        return self.__wiki_project_repository.get_list()

    def get_page(self, params: WikiProjectPageParamsModel) -> Pagination:
        return self.__wiki_project_repository.page(
            page_index=params.page_index,
            page_size=params.page_size,
            search=params.search,
        )

    def get_public_page(self, params: WikiProjectPageParamsModel) -> Pagination:
        return self.__wiki_project_repository.get_public_page(
            page_index=params.page_index,
            page_size=params.page_size,
            search=params.search,
        )

    def edit(
            self,
            params: EditWikiProjectParamsModel,
            current_user_info: ValidateTokenResModel,
    ) -> str:
        dup = self.__wiki_project_repository.get_exist(
            code=params.code,
            project_id=params.project_id,
        )
        if dup:
            raise BusinessError('项目编码已存在')
        if params.project_id:
            project = self.get_by_id(project_id=params.project_id)
            if project.code == HOME_WIKI_PROJECT_CODE and params.code != HOME_WIKI_PROJECT_CODE:
                raise BusinessError('首页项目编码不可修改')
            project.code = params.code
            project.name = params.name
            project.desc = params.desc
            project.operator_category = EnumOperatorCategory.UNION_USER.value
            project.operator = current_user_info.union_user_info.id
            self.__wiki_project_repository.update(model=project)
            return project.id
        project = WikiProjectModel(
            id=str(uuid.uuid4()),
            code=params.code,
            name=params.name,
            desc=params.desc,
            is_deleted=False,
            operator_category=EnumOperatorCategory.UNION_USER.value,
            operator=current_user_info.union_user_info.id,
        )
        self.__wiki_project_repository.insert(model=project)
        return project.id

    def delete(self, params: DeleteWikiProjectParamsModel):
        project = self.get_by_id(project_id=params.project_id)
        if project.code == HOME_WIKI_PROJECT_CODE:
            raise BusinessError('首页项目不可删除')
        project.is_deleted = True
        self.__wiki_project_repository.update(model=project)
