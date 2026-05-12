# WEB 端 UI 规范

## 色彩

| 用途 | 值 |
|---|---|
| 主色（渐变起点） | `from-emerald-500` / `from-teal-500` |
| 主色（渐变终点） | `to-teal-600` / `to-cyan-600` |
| 页面背景 | `bg-gradient-to-br from-gray-50 to-gray-100/50` |
| 卡片背景 | `bg-white` |
| 正文文字 | `text-gray-700` |
| 次要文字 | `text-gray-500` |
| 辅助文字 | `text-gray-400` |
| 边框 | `border-gray-100` / `border-gray-200` |
| 危险色 | `text-red-500` / `text-red-600` |
| 成功色 | `text-green-500` / `text-green-600` |

## 布局

- 页面最外层：`h-full flex flex-col min-h-0 overflow-hidden`
- 顶栏：`shrink-0 px-6 py-5 bg-white shadow-sm border-b border-gray-100`
- 内容区：`flex-1 min-h-0 px-6 py-6 overflow-hidden`
- 卡片：`bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden`

## 图标区块（页面标题左侧）

```html
<div class="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl
            flex items-center justify-center text-white shadow-lg shadow-emerald-500/25
            transform rotate-3 transition-transform hover:rotate-6">
  <Icon .../>
</div>
```

## 模态框

- 宽度：按内容定，常用 `480px` / `520px` / `640px` / `900px`
- `preset="card"`，`:bordered="false"`，`:mask-closable` 根据场景决定
- Header：图标区块（10×10，渐变背景，rounded-xl）+ 标题文字
- Footer：`flex justify-end gap-3`，取消按钮在左，主操作在右

### 模态框高度与滚动规范

- **内容可能超出视口时，必须限制高度并启用滚动，不允许撑破 modal**
- 固定布局（搜索+树+面板等）：内容区使用 flex 填充，高度用 `clamp(最小, calc(85vh - header/footer高度), 最大)` ；内部滚动区加 `flex-1 min-h-0 overflow-y-auto`
- 列表类内容（表单内动态列表等）：列表容器加 `max-height: min(50vh, 360px); overflow-y: auto`，操作按钮放在列表容器**外部下方**，始终可见
- 禁止对整个 modal 或 card content 使用固定像素高度；应优先用 `vh` + `clamp` 保证在不同屏幕分辨率下均可用
- **滚动条紧贴 modal 右侧**的实现方式：
  1. `n-modal` 加 `:content-style="{ paddingRight: 0 }"` 去掉 card 右内边距（NaiveUI 默认 24px）
  2. 内容外层 div 加回 `padding-right: 24px`（保证按钮等非滚动元素的右边距）
  3. 滚动容器加 `margin-right: -24px; padding-right: 10px`：负 margin 填满 card 右侧空间，padding-right 保留内容与滚动条的视觉间距

## 表单

- `label-placement="left"`，`label-width="auto"` 或固定像素
- 必填项标注使用 Naive UI 原生 `required` 或自定义 `*` 标记
- 输入框清空按钮统一启用 `clearable`

## 复选框

- 树形多选器中的复选框：方形，需同时覆盖 CSS 变量和实际属性（通过 `:deep` 覆盖）：
  ```scss
  :deep(.dept-tree) {
    .n-checkbox { --n-border-radius: 3px !important; }
    .n-checkbox-box, .n-checkbox-box__border { border-radius: 3px !important; }
  }
  ```
- 普通列表复选框：使用 Naive UI 默认圆角（`NCheckbox` 不单独覆盖）

## 表格

- `:bordered="false"`，`striped`
- 表头：`background: linear-gradient(to bottom, #fafafa, #f5f5f5)`，`font-weight: 600`
- 单元格内距：`padding: 16px`
- 悬停行：`background: linear-gradient(to right, #f9fafb, #f3f4f6)`
- 滚动条统一样式（宽 8px，`#d1d5db` → hover `#9ca3af`）

## 分页

- `show-size-picker`，可选 `[20, 50, 100, 200, 300]`
- 放置于卡片底部 `border-t border-gray-100` 分隔线下方

## 按钮

- 主操作：`type="primary"`
- 危险操作：`type="error"` 或 `type="primary"` 配合确认弹窗
- 图标按钮使用 `<template #icon>` 插槽，不直接传 icon prop

## 空状态

```html
<div class="flex flex-col items-center justify-center py-16">
  <div class="w-32 h-32 bg-gray-100 rounded-full flex items-center justify-center mb-4">
    <Icon class="text-gray-400" :width="48" :height="48"/>
  </div>
  <p class="text-gray-500 text-lg">暂无记录</p>
</div>
```

## 滚动条规范

- 滚动条必须在容器**内部**，不允许覆盖在内容上
- 可滚动容器须加 `padding-right: 4px`，为滚动条留出视觉间距
- 滚动条 track 背景用 `transparent`（modal 内）或 `#f5f5f5`（页面级列表）

```scss
/* modal 内滚动容器 */
.scrollable {
  overflow-y: auto;
  padding-right: 4px;

  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-track { background: transparent; border-radius: 3px; }
  &::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; &:hover { background: #9ca3af; } }
}

/* 页面级大列表 */
.page-scroll {
  &::-webkit-scrollbar { width: 8px; height: 8px; }
  &::-webkit-scrollbar-track { background: #f5f5f5; border-radius: 4px; }
  &::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 4px; &:hover { background: #9ca3af; } }
}
```
