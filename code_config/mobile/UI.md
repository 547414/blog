# MOBILE 端 UI 规范

## 色彩

| 用途 | 值 |
|---|---|
| 主色 | `#0d9488`（teal-600） |
| 主色浅 | `#14b8a6`（teal-500） |
| 页面背景 | `bg-gray-50` |
| 卡片背景 | `bg-white` |
| 正文文字 | `text-gray-800` |
| 次要文字 | `text-gray-500` |
| 辅助文字 | `text-gray-400` |
| 边框/分割线 | `border-gray-100` |
| 危险色 | `text-red-500` |
| 成功色 | `text-green-500` |

## 布局

- 页面根节点：`min-h-screen bg-gray-50`
- 顶部导航：Vant `NavBar`，标题居中，左侧返回按钮
- 内容区留底部安全距离：`pb-safe` 或 `padding-bottom: env(safe-area-inset-bottom)`
- 列表页底部操作栏固定：`fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-4 py-3`

## 卡片

```html
<div class="bg-white rounded-xl mx-4 mb-3 shadow-sm overflow-hidden">
  ...
</div>
```

- 圆角：`rounded-xl`（12px）
- 内距：`p-4`
- 阴影：`shadow-sm`
- 外边距：`mx-4 mb-3`

## 表单

- 使用 Vant `CellGroup` + `Field` 组合
- `input-align="right"` 对齐输入内容
- 必填项使用 Vant `required` 属性
- 提交按钮：`<van-button type="primary" block round>`，放置于表单底部

## 列表

- 使用 Vant `List`（虚拟滚动场景）或 `v-for` + 自定义卡片
- 下拉刷新：Vant `PullRefresh`
- 空状态：Vant `Empty`，`description` 传中文描述

## 弹窗 / 选择器

- 底部弹出：Vant `Popup`，`position="bottom"`，`round`
- 确认/取消操作：Vant `ActionSheet` 或自定义底部按钮栏
- 选项选择：Vant `Picker`
- 日期选择：Vant `DatePicker`

## 复选框 / 单选

- 列表多选：Vant `Checkbox` + `CheckboxGroup`，复选框为**方形**（`shape="square"`）
- 单选：Vant `Radio` + `RadioGroup`

## 按钮

- 主操作：`type="primary"`，页面级操作用 `block`
- 圆形小图标按钮：`icon` prop + `round` + `size="small"`
- 危险操作需二次确认：Vant `Dialog.confirm`

## 顶部状态栏适配

- 顶部固定元素加 `padding-top: env(safe-area-inset-top)`
- 使用 Vant `NavBar` 时 `safe-area-inset-top` 属性自动处理

## 加载状态

- 列表加载：Vant `List` 的 `loading` / `finished` 状态
- 操作加载：Vant `Button` 的 `loading` prop
- 全屏加载：Vant `Overlay` + `Loading`
