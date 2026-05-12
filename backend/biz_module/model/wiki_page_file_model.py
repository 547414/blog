from typing import Optional

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasisModel


class WikiPageFileModel(BasicVersionModel):
    page_id: str = Field(..., description="所属页面ID")
    file_info_id: Optional[str] = Field(None, description="文件ID")
    file_name: Optional[str] = Field(None, description="文件名称")
    file_type: Optional[str] = Field(None, description="文件类型")
    file_size: Optional[int] = Field(None, description="文件大小")
    bucket_name: Optional[str] = Field(None, description="存储桶名称")
    object_name: Optional[str] = Field(None, description="对象名称")
    file_object_name: Optional[str] = Field(None, description="文件对象名称")
    file_hash: Optional[str] = Field(None, description="文件哈希")
    url: Optional[str] = Field(None, description="文件访问URL")
    is_deleted: bool = Field(False, description="是否删除")


class SaveWikiPageFileParamsModel(BasisModel):
    page_id: str = Field(..., description="所属页面ID")
    file_info_id: Optional[str] = Field(None, description="文件ID")
    file_name: Optional[str] = Field(None, description="文件名称")
    file_type: Optional[str] = Field(None, description="文件类型")
    file_size: Optional[int] = Field(None, description="文件大小")
    bucket_name: Optional[str] = Field(None, description="存储桶名称")
    object_name: Optional[str] = Field(None, description="对象名称")
    file_object_name: Optional[str] = Field(None, description="文件对象名称")
    file_hash: Optional[str] = Field(None, description="文件哈希")
    url: Optional[str] = Field(None, description="文件访问URL")


class DeleteWikiPageFileParamsModel(BasisModel):
    file_id: str = Field(..., description="附件ID")


class GetWikiPageFileListParamsModel(BasisModel):
    page_id: str = Field(..., description="页面ID")
