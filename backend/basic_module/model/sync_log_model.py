from datetime import datetime
from typing import Optional

from pydantic import Field

from basic.model.basic_model import BasicVersionModel


class SyncLogModel(BasicVersionModel):
    sync_type: str = Field(..., description="同步类型")
    total_records: Optional[int] = Field(0, description="总记录数")
    successful_records: Optional[int] = Field(0, description="成功记录数")
    failed_records: Optional[int] = Field(0, description="失败记录数")
    sync_time: Optional[datetime] = Field(datetime.now(), description="同步时间")
    details: Optional[str] = Field(None, description="同步详情")
