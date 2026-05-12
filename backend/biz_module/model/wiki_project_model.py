from datetime import datetime
from typing import Optional

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasisModel


HOME_WIKI_PROJECT_CODE = 'HOME_PROJECT'


class WikiProjectModel(BasicVersionModel):
    code: str = Field(..., description="项目编码")
    name: str = Field(..., description="项目名称")
    is_deleted: bool = Field(False, description="是否删除")


class PublicWikiProjectItemModel(BasicVersionModel):
    code: str = Field(..., description="项目编码")
    name: str = Field(..., description="项目名称")
    is_deleted: bool = Field(False, description="是否删除")
    wiki_count: int = Field(0, description="公开Wiki数量")
    latest_updated_at: Optional[datetime] = Field(None, description="最近Wiki更新时间")


class EditWikiProjectParamsModel(BasisModel):
    project_id: Optional[str] = Field(None, description="项目ID，为空时新建")
    code: str = Field(..., description="项目编码")
    name: str = Field(..., description="项目名称")
    desc: Optional[str] = Field(None, description="项目描述")


class DeleteWikiProjectParamsModel(BasisModel):
    project_id: str = Field(..., description="项目ID")


class WikiProjectPageParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="分页大小")
    search: Optional[str] = Field(None, description="搜索关键字")
