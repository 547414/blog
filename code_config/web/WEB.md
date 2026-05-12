# WEB 端约定

## 总则

- 样式：Tailwind CSS + SCSS，搜索框不加 `paddingLeft`
- Vue 单文件组件样式必须使用 `<style scoped lang="scss">`；禁止使用未 scoped 的 `<style lang="scss">`，需要命中 Teleport/组件库全局 DOM 时在 scoped 样式内使用 `:global(...)`
- 语法：Vue `<script setup>` 语法糖
- API 调用：`.then()` 链式写法，**不用** `async/await`
- 组件库：Naive UI
- `v-model` 只能绑定可赋值的表达式，带 `??` / `||` 等运算符时用 `:value` + `@update:value` 替代
- 函数参数中的对象类型不要内联声明，使用 `interface` 封装
- API 的嵌套对象结构（如 `data`、`fixedValue`、`defaultValue`）也不要内联声明；非必要不用 `any`，优先明确 `interface` / 联合类型
- 若数据结构来自接口返回或请求参数，`interface/type` 定义在对应 `src/api/*Api.ts` 中，组件内通过 `import type` 引用，不重复声明
- 组件内 `ref` / `reactive` 持有对象、数组等结构时，类型必须先用 `interface` 定义并通过 `ref<XxxState>({...})` 显式标注；禁止 `ref({field: null as string | null})` 这种字面量内的 `as` 断言
- 弹窗 state、表单 state、上下文菜单 state 等"局部 UI 状态对象"应抽出 `interface`（如 `XxxModalState`、`XxxEditForm`），不要让类型靠 TS 推断
- 调用 API 函数传入对象字面量参数时，必须先用 `const params: XxxParams = {...}` 显式声明类型再传，禁止 `apiXxx({a, b, c})` 直接内联；`XxxParams` 来自对应 `*Api.ts`
- 函数 emit 的 payload、自定义事件回调的入参也必须用 `interface` 类型化（如 `interface TreeContextMenuPayload {...}`），不允许 `any`

## 命名规范

- **列表字段禁止使用英文复数形式**（`depts`、`users`、`items` 等）；一律用 `List` 后缀，如 `deptList`、`userList`；ID 列表用 `IdList`，禁止 `deptIds` 这类写法

## UI 规范

详见 [UI.md](UI.md)

## api 约定

详见 [API.md](API.md)
