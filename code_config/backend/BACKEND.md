# 后端约定

## 模块依赖规则

依赖方向严格单向，禁止反向依赖：

```
basic → basic_module → biz_module
                    → bei_sen_module
```

- `biz_module` / `bei_sen_module` 可依赖 `basic` / `basic_module`
- `biz_module` 可依赖 `bei_sen_module`（跨平行模块允许）
- **`bei_sen_module` 严禁依赖 `biz_module`**
- 违反规则时，将跨模块逻辑提取到上层模块（`biz_module`）中新建服务承接

### Repository/Container 归属规则

- **Repository 必须声明在其 entity 所在的模块**；其他模块需要时，从该模块的 container 引用，不得重复创建 Factory
- 例：`ConfigDictRepository` 的 entity 在 `basic_module`，则其他 container 应写 `config_dict_repository = basic_module_container.config_dict_repository`，不得再写 `providers.Factory(ConfigDictRepository, session=session)`

## 命名规范

- **列表字段禁止使用英文复数形式**（`depts`、`users`、`items` 等）；一律用 `_list` 后缀，如 `dept_list`、`user_list`；ID 列表用 `_id_list`，禁止 `dept_ids` 这类写法

## 总则

- **分层**：`entity/` → `model/` → `repository/` → `service/` → `router/`
- **依赖注入**：`dependency-injector`，容器 `app/containers.py` → 各模块 `xxx_module_container.py`
- **配置**：`app_config.toml` 的 `settings.active` 决定环境，加载 `config/app_{env}_config.toml`
- **事务**：`UnitOfWork` 上下文管理器管理 SQLAlchemy session
- **类型约束**：`list` 用 `List`，`dict` 用 `Dict`（从 typing 导入）
- **SQL**：使用三引号 `"""..."""` 包裹；`sql +=` 追加条件、排序、分页等片段时也必须使用三引号，不允许单引号/双引号直接拼接 SQL 片段
- **枚举参数**：SQL 参数如果来源于枚举，必须传 `EnumXxx.XXX.value`；参数名与 SQL 占位符必须写成有语义的名字，如 `assessment_plan_status`、`menu_type`，禁止直接写成泛化的 `status`、`type` 这类枚举占位符
- **数据封装**：处理或取数据前用 model 封装，避免下划线/驼峰混乱
- **JSON/嵌套结构**：`data`、`fixed_value`、快照等结构优先用 `BasisModel` 子 model 封装；前端驼峰、后端下划线依赖 `basic/model/basic_model.py` 自动转换，非必要不要裸 `Dict[str, Any]`
- **方法调用**：router/service/repository 中调用方法必须写明参数名（`func(param_name=value)`）
- **返回给前端**：数据格式 必须使用model封装

## 各层规范
``
- [ENTITY.md](ENTITY.md) — entity 层
- [MODEL.md](MODEL.md) — model 层
- [REPOSITORY.md](REPOSITORY.md) — repository 层
- [SERVICE.md](SERVICE.md) — service 层
- [ROUTER.md](ROUTER.md) — router 层
- [ENUM.md](ENUM.md) — 枚举
