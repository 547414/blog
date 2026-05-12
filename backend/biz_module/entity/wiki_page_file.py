from sqlalchemy import Column, String, Boolean, INTEGER, Index, Text

from basic.entity.basic_entity import BasicEntity


class WikiPageFileEntity(BasicEntity):
    __tablename__ = 'bt_wiki_page_file'
    __table_args__ = (
        Index('idx_bt_wiki_page_file_page_id', 'page_id'),
        {"comment": "Wiki页面附件表"}
    )

    page_id = Column(String(40), nullable=False, comment='所属页面ID')
    file_info_id = Column(String(40), nullable=True, comment='文件ID')
    file_name = Column(String(500), nullable=True, comment='文件名称')
    file_type = Column(String(255), nullable=True, comment='文件类型')
    file_size = Column(INTEGER, nullable=True, comment='文件大小')
    bucket_name = Column(String(500), nullable=True, comment='存储桶名称')
    object_name = Column(Text, nullable=True, comment='对象名称')
    file_object_name = Column(Text, nullable=True, comment='文件对象名称')
    file_hash = Column(String(255), nullable=True, comment='文件哈希')
    url = Column(Text, nullable=True, comment='文件访问URL')
    is_deleted = Column(Boolean, nullable=False, default=False, comment='是否删除')
