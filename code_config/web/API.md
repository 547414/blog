# web api 约定

参考：`web/src/api/menuApi.ts`

## 规则

- 文件名 `xxxApi.ts`，放在 `src/api/`
- `const prefix = '/xxx'`，与后端 router 模块名对应
- 接口（interface）用 camelCase，字段与后端 model `model_dump()` 输出的 camelCase 一致
- 接口返回值、请求参数及其复用的数据结构，统一定义在对应 `xxxApi.ts` 中；页面/组件通过 `import type` 复用，不在组件内重复声明
- 响应类型继承 `Response`（从 `@/utils/requestTypes.ts` 导入）
- 导出 `apiXxxAction` 格式的函数，返回 `Promise<XxxResponse>`
- **API 函数体必须通过 `axios` 真实发起请求**（`axios.get` / `axios.post` 等），禁止 `Promise.resolve({...})` 等本地 mock；接口未实现时由后端先返回空数据，前端不在 Api 文件里编造 mock
- 函数入参即使只有一个 `id` 字段，也要先抽 `interface`（如 `PageIdParams { pageId: string }`），不要写成 `(params: { pageId: string })` 内联类型
- 文件下载用 `responseType: 'blob'`

## 示例骨架

```typescript
import axios from '@/utils/request';
import { Response } from '@/utils/requestTypes.ts';

const prefix = '/xxx';

export interface XxxDetail {
    id: string;
    name: string;
}

export interface XxxPageParams {
    pageIndex: number;
    pageSize: number;
    search: string | null;
}

export interface XxxPageResponse extends Response {
    data: { totalCount: number; data: XxxDetail[] };
}

export const apiGetXxxPage = (params: XxxPageParams): Promise<XxxPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export const apiGetXxxDetail = (id: string): Promise<Response> => {
    return axios.get(`${prefix}/detail/${id}`);
};
```
