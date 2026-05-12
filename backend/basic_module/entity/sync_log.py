import datetime

from sqlalchemy import Column, String, Text, DateTime, text, Integer

from basic.entity.basic_entity import BasicEntity


class SyncLogEntity(BasicEntity):
    __tablename__ = 'ct_sync_log'
    __table_args__ = (
        {"comment": "同步日志表"}
    )

    sync_type = Column(String(255), nullable=False, comment='同步类型')
    total_records = Column(Integer, nullable=False, comment='总记录数')
    successful_records = Column(Integer, nullable=False, comment='成功')
    failed_records = Column(Integer, nullable=False, comment='失败')
    sync_time = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        comment='同步时间'
    )
    details = Column(Text, nullable=False, comment='同步详情')
