import uuid

from basic.error.base_error import BusinessError
from basic.model.basic_model import EnumOperatorCategory
from basic_module.model.validate_token_model import ValidateTokenResModel
from biz_module.model.wiki_page_file_model import (
    WikiPageFileModel,
    SaveWikiPageFileParamsModel,
    DeleteWikiPageFileParamsModel,
    GetWikiPageFileListParamsModel,
)
from biz_module.repository.wiki_page_file_repository import WikiPageFileRepository


class WikiPageFileService:
    def __init__(
            self,
            wiki_page_file_repository: WikiPageFileRepository
    ):
        self.__wiki_page_file_repository = wiki_page_file_repository

    def save(
            self,
            params: SaveWikiPageFileParamsModel,
            current_user_info: ValidateTokenResModel
    ):
        model = WikiPageFileModel(
            id=str(uuid.uuid4()),
            page_id=params.page_id,
            file_info_id=params.file_info_id,
            file_name=params.file_name,
            file_type=params.file_type,
            file_size=params.file_size,
            bucket_name=params.bucket_name,
            object_name=params.object_name,
            file_object_name=params.file_object_name,
            file_hash=params.file_hash,
            url=params.url,
            is_deleted=False,
            operator_category=EnumOperatorCategory.UNION_USER.value,
            operator=current_user_info.union_user_info.id,
        )
        self.__wiki_page_file_repository.insert(model=model)
        return model.id

    def detail(self, file_id: str):
        file = self.__wiki_page_file_repository.get_by_id(
            file_id=file_id,
        )
        if not file:
            raise BusinessError('附件不存在')
        return file

    def get_list(self, params: GetWikiPageFileListParamsModel):
        return self.__wiki_page_file_repository.get_list_by_page_id(
            page_id=params.page_id
        )

    def delete(self, params: DeleteWikiPageFileParamsModel):
        exist = self.detail(
            file_id=params.file_id,
        )
        exist.is_deleted = True
        self.__wiki_page_file_repository.update(model=exist)
