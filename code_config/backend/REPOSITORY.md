# repository 约定

参考：`backend/basic_module/repository/menu_repository.py`

## 规则

- 继承 `BaseRepository`，构造函数接收 `session: Session` 并调用 `super().__init__(session)`
- **insert / update / delete_by_id** 为固定模板，不允许修改：
    - `insert` → `self.add(model=, entity=)`
    - `update` → `self.update_entity(entity=, entity_id=, model=)`
    - `delete_by_id` → `self.delete(entity=, entity_id=)`
- **禁止**直接使用 `self.session`，必须通过 `BaseRepository` 提供的方法操作数据
- **禁止使用 `execute_sql`**；新增、更新、删除必须通过 `add` / `update_entity` / `delete` 封装方法，查询必须通过 `get_by_params` / `get_all_by_params` / `get_page`
- 查询方法使用 `get_by_params` / `get_all_by_params` / `get_page`，SQL 用三引号包裹
- `sql +=` 追加 `WHERE` 条件、`ORDER BY`、`LIMIT` 等 SQL 片段时，也必须使用三引号包裹
- `ORDER BY` 升序为默认行为，**禁止显式写 `ASC`**（如 `ORDER BY created_at ASC` 应写成 `ORDER BY created_at`）；降序保留 `DESC`
- SQL 参数如果来源于枚举，必须显式传 `.value`，且参数名/占位符名要带具体语义，例如 `assessment_plan_status`，不要直接写 `status`
- 方法调用必须写明参数名，多参数时每个参数独占一行（包括单参数）
- 返回 ViewModel 的查询写独立方法（如 `find_page` / `get_view_by_id`）

### 类型与参数

- 可选参数禁止 `def foo(x: str = None)` 这种写法，必须显式写 `Optional[T]`：`def foo(x: Optional[str] = None)`
- `params` 字典如有"先占位 None，再按条件赋值字符串"的用法，必须显式标注 `params: Dict[str, Any] = {...}`，避免 IDE 推断成 `Dict[str, None]`
- 当 `search` / `keyword` 等可选过滤参数为 `None` 时，禁止拼出 `f'%{search}%'` 让 SQL 里出现 `%None%`；要么只在 `if search:` 分支内赋值，要么保持占位为 `None`

### 涉及聚合的查询

- **禁止** `SELECT t.*` 配合 `GROUP BY t.id` —— 部分数据库会报 "columns are invalid in the select list because they are not contained in either an aggregate function or the GROUP BY clause"
- 涉及聚合的分页查询，统一改用**派生表 / EXISTS 子查询**：先在子查询中按主表 ID 聚合出 `count` / `max` 等列，再 INNER JOIN 回主表，外层不需要 GROUP BY，从而可以安全使用 `SELECT t.*`
- 若过滤条件涉及"主表字段 OR 子表存在匹配记录"，子表的匹配条件用 `EXISTS (SELECT 1 FROM ...)` 表达，避免在主聚合 JOIN 上叠加条件导致计数错乱

## 容器注册

在对应的 `xxx_module_container.py` 中用 `providers.Factory` 注册：
```python
xxx_repository = providers.Factory(
  XxxRepository
)
```

## 示例骨架

```python
from typing import List, Optional
from enum import Enum
from sqlalchemy.orm import Session
from basic.repository.base_repository import BaseRepository
from xxx_module.entity.xxx import XxxEntity
from xxx_module.model.xxx_model import XxxModel, XxxViewModel


class EnumXxxStatus(Enum):
    ENABLED = "ENABLED"


class XxxRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: XxxModel):
        return self.add(
            model=model,
            entity=XxxEntity
        )

    def update(self, model: XxxModel):
        return self.update_entity(
            entity=XxxEntity,
            entity_id=model.id,
            model=model
        )

    def delete_by_id(self, data_id: str):
        return self.delete(
            entity=XxxEntity,
            entity_id=data_id
        )

    def get_by_id(self, data_id: str) -> Optional[XxxModel]:
        sql = """
        SELECT * FROM bt_xxx WHERE id = :data_id
        """

        return self.get_by_params(
            sql=sql,
            model=XxxModel,
            params={
                "data_id": data_id
            }
        )

    def get_list(self, status: str = None) -> List[XxxModel]:
        sql = """
        SELECT * FROM bt_xxx
        WHERE is_deleted = false
        """
        params = {}
        if status:
            sql += """
            AND status = :xxx_status
            """
            params["xxx_status"] = status

        sql += """
        ORDER BY created_at DESC
        """

        return self.get_all_by_params(
            sql=sql,
            model=XxxModel,
            params=params
        )

    def get_enabled_list(self) -> List[XxxModel]:
        sql = """
        SELECT * FROM bt_xxx
        WHERE is_deleted = false
          AND status = :xxx_enabled_status
        ORDER BY created_at DESC
        """
        params = {
            "xxx_enabled_status": EnumXxxStatus.ENABLED.value
        }

        return self.get_all_by_params(
            sql=sql,
            model=XxxModel,
            params=params
        )
```
