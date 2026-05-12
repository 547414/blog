import axios from '@/utils/request';
import {Response} from '@/utils/requestTypes.ts';

const prefix = '/wiki_page';

export interface WikiPageTreeItem {
    id: string;
    title: string;
    seq: number;
    parentId: string | null;
    isPublic: boolean;
    requireAuth: boolean;
    accessCode: string | null;
    childList: WikiPageTreeItem[];
}

export interface WikiPageTreeResponse extends Response {
    data: WikiPageTreeItem[];
}

export interface PublicWikiSearchItem {
    pageId: string;
    pageTitle: string;
    projectId: string;
    projectName: string;
    projectCode: string;
    requireAuth: boolean;
}

export interface PublicWikiSearchResultData {
    dataList: PublicWikiSearchItem[];
    hasMore: boolean;
}

export interface PublicWikiSearchResponse extends Response {
    data: PublicWikiSearchResultData;
}

export interface PublicWikiSearchParams {
    search: string;
    page: number;
    pageSize: number;
}

export interface GetWikiPageTreeParams {
    projectId?: string | null;
}

export interface PageIdParams {
    pageId: string;
}

export interface FileIdParams {
    fileId: string;
}

export interface WikiPageDetail {
    id: string;
    projectId?: string | null;
    parentId: string | null;
    slug?: string | null;
    title: string;
    content: string | null;
    seq: number;
    isPublic: boolean;
    requireAuth: boolean;
    accessCode: string | null;
    createdAt: string | null;
    updatedAt: string | null;
}

export interface WikiPageDetailResponse extends Response {
    data: WikiPageDetail;
}

export interface EditWikiPageParams {
    pageId: string | null;
    projectId?: string | null;
    parentId: string | null;
    title: string;
    content: string | null;
    seq: number;
    isPublic?: boolean;
    requireAuth?: boolean;
    accessCode?: string | null;
}

export interface EditWikiPageResponse extends Response {
    data: string;
}

export interface DeleteWikiPageParams {
    pageId: string;
}

export interface SetWikiPageVisibilityParams {
    pageId: string;
    isPublic: boolean;
    requireAuth?: boolean;
    accessCode?: string | null;
}

export interface SaveWikiPageTreeParams {
    projectId?: string | null;
    pageList: WikiPageTreeItem[];
}

export const apiGetWikiPageTree = (params?: GetWikiPageTreeParams): Promise<WikiPageTreeResponse> => {
    return axios.get(`${prefix}/tree`, {
        params: {
            projectId: params?.projectId,
        },
    });
};

export const apiGetWikiPageDetail = (pageId: string): Promise<WikiPageDetailResponse> => {
    return axios.get(`${prefix}/detail/${pageId}`);
};

export const apiEditWikiPage = (params: EditWikiPageParams): Promise<EditWikiPageResponse> => {
    return axios.post(`${prefix}/edit`, params);
};

export const apiDeleteWikiPage = (params: DeleteWikiPageParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};

export const apiSetWikiPageVisibility = (params: SetWikiPageVisibilityParams): Promise<Response> => {
    return axios.post(`${prefix}/visibility/set`, params);
};

export const apiSaveWikiPageTree = (params: SaveWikiPageTreeParams): Promise<Response> => {
    return axios.post(`${prefix}/tree/save`, params);
};

export const apiGetPublicWikiPageTree = (projectId?: string | null): Promise<WikiPageTreeResponse> => {
    return axios.get(projectId ? `${prefix}/public/tree/${projectId}` : `${prefix}/public/tree`);
};

export const apiGetPublicWikiPageDetail = (pageId: string, authCode?: string | null, projectId?: string | null): Promise<WikiPageDetailResponse> => {
    return axios.get(`${prefix}/public/detail/${pageId}`, {
        params: {
            authCode,
            projectId,
        },
    });
};

export const apiSearchPublicWiki = (params: PublicWikiSearchParams): Promise<PublicWikiSearchResponse> => {
    return axios.get(`${prefix}/public/search`, {
        params,
    });
};

export interface WikiPageFileDetail {
    id: string;
    pageId: string;
    fileInfoId: string | null;
    fileName: string | null;
    fileType: string | null;
    fileSize: number | null;
    bucketName: string | null;
    objectName: string | null;
    url: string | null;
    createdAt: string | null;
}

export interface WikiPageFileListResponse extends Response {
    data: WikiPageFileDetail[];
}

export interface SaveWikiPageFileParams {
    pageId: string;
    fileInfoId: string | null;
    fileName: string | null;
    fileType: string | null;
    fileSize: number | null;
    bucketName: string | null;
    objectName: string | null;
    fileObjectName: string | null;
    fileHash: string | null;
    url: string | null;
}

export const apiGetWikiPageFileList = (params: PageIdParams): Promise<WikiPageFileListResponse> => {
    return axios.post(`${prefix}/file/list`, params);
};

export const apiSaveWikiPageFile = (params: SaveWikiPageFileParams): Promise<Response> => {
    return axios.post(`${prefix}/file/save`, params);
};

export const apiDeleteWikiPageFile = (params: FileIdParams): Promise<Response> => {
    return axios.post(`${prefix}/file/delete`, params);
};

export const apiGetPublicWikiPageFileList = (pageId: string, authCode?: string | null, projectId?: string | null): Promise<WikiPageFileListResponse> => {
    return axios.get(`${prefix}/public/file/list/${pageId}`, {
        params: {
            authCode,
            projectId,
        },
    });
};

export interface WikiPageHistoryItem {
    id: string;
    pageId: string;
    editor: string | null;
    editorName: string | null;
    versionNo: number;
    createdAt: string | null;
}

export interface WikiPageHistoryListResponse extends Response {
    data: WikiPageHistoryItem[];
}

export const apiGetWikiPageHistoryList = (params: PageIdParams): Promise<WikiPageHistoryListResponse> => {
    return axios.get(`${prefix}/history/list/${params.pageId}`);
};
