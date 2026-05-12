from sqlalchemy import Column, String, Boolean, INTEGER, Index, Text

from basic.entity.basic_entity import BasicEntity


class WikiPageEntity(BasicEntity):
    __tablename__ = 'bt_wiki_page'
    __table_args__ = (
        Index('idx_bt_wiki_page_project_id', 'project_id'),
        Index('idx_bt_wiki_page_parent_id', 'parent_id'),
        {"comment": "Wiki页面表"}
    )

    creator = Column(String(40), nullable=True, comment='创建者, 联合用户ID')
    project_id = Column(String(40), nullable=True, comment='所属Wiki项目ID')
    parent_id = Column(String(40), nullable=True, comment='父页面ID')
    title = Column(String(255), nullable=False, comment='页面标题')
    content = Column(Text, nullable=True, comment='富文本内容')
    seq = Column(INTEGER, nullable=False, default=0, comment='排序')
    is_public = Column(Boolean, nullable=False, default=False, comment='是否公开')
    require_auth = Column(Boolean, nullable=False, default=False, comment='是否需要授权码')
    access_code = Column(String(255), nullable=True, comment='访问授权码')
    is_deleted = Column(Boolean, nullable=False, default=False, comment='是否删除')
