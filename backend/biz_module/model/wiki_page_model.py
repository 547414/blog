from typing import Optional, List

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasisModel


class WikiPageModel(BasicVersionModel):
    creator: Optional[str] = Field(None, description="创建者, 联合用户ID")
    project_id: Optional[str] = Field(None, description="所属Wiki项目ID")
    parent_id: Optional[str] = Field(None, description="父页面ID")
    title: str = Field(..., description="页面标题")
    content: Optional[str] = Field(None, description="富文本内容")
    seq: int = Field(0, description="排序")
    is_public: bool = Field(False, description="是否公开")
    require_auth: bool = Field(False, description="是否需要授权码")
    access_code: Optional[str] = Field(None, description="访问授权码")
    is_deleted: bool = Field(False, description="是否删除")


class EditWikiPageParamsModel(BasisModel):
    page_id: Optional[str] = Field(None, description="页面ID，为空时新建")
    project_id: Optional[str] = Field(None, description="所属Wiki项目ID")
    parent_id: Optional[str] = Field(None, description="父页面ID")
    title: str = Field(..., description="页面标题")
    content: Optional[str] = Field(None, description="富文本内容")
    seq: int = Field(0, description="排序")
    is_public: bool = Field(False, description="是否公开")
    require_auth: bool = Field(False, description="是否需要授权码")
    access_code: Optional[str] = Field(None, description="访问授权码")


class SetWikiPageVisibilityParamsModel(BasisModel):
    page_id: str = Field(..., description="页面ID")
    is_public: bool = Field(False, description="是否公开")
    require_auth: bool = Field(False, description="是否需要授权码")
    access_code: Optional[str] = Field(None, description="访问授权码")


class DeleteWikiPageParamsModel(BasisModel):
    page_id: str = Field(..., description="页面ID")


class WikiPageTreeItemModel(BasisModel):
    id: str = Field(..., description="页面ID")
    project_id: Optional[str] = Field(None, description="所属Wiki项目ID")
    title: str = Field(..., description="页面标题")
    seq: int = Field(0, description="排序")
    parent_id: Optional[str] = Field(None, description="父页面ID")
    is_public: bool = Field(False, description="是否公开")
    require_auth: bool = Field(False, description="是否需要授权码")
    access_code: Optional[str] = Field(None, description="访问授权码")
    child_list: List['WikiPageTreeItemModel'] = Field(default_factory=list, description="子页面列表")


WikiPageTreeItemModel.model_rebuild()


class SaveWikiPageTreeParamsModel(BasisModel):
    project_id: Optional[str] = Field(None, description="所属Wiki项目ID")
    page_list: List[WikiPageTreeItemModel] = Field(default_factory=list, description="页面树")


class PublicWikiSearchItemModel(BasisModel):
    page_id: str = Field(..., description="页面ID")
    page_title: str = Field(..., description="页面标题")
    project_id: str = Field(..., description="项目ID")
    project_name: str = Field(..., description="项目名称")
    project_code: str = Field(..., description="项目编码")
    require_auth: bool = Field(False, description="是否需要授权码")


class PublicWikiSearchResultModel(BasisModel):
    data_list: List[PublicWikiSearchItemModel] = Field(default_factory=list, description="搜索结果")
    has_more: bool = Field(False, description="是否还有下一页")
