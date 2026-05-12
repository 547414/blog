from sqlalchemy import Column, String, Boolean, INTEGER, Index

from basic.entity.basic_entity import BasicEntity


class WikiProjectEntity(BasicEntity):
    __tablename__ = 'bt_wiki_project'
    __table_args__ = (
        Index('idx_bt_wiki_project_code', 'code'),
        {"comment": "Wiki项目表"}
    )

    code = Column(String(255), nullable=False, comment='项目编码')
    name = Column(String(255), nullable=False, comment='项目名称')
    seq = Column(INTEGER, nullable=False, default=0, server_default='0', comment='排序')
    is_deleted = Column(Boolean, nullable=False, default=False, comment='是否删除')
