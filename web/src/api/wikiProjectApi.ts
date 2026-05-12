import axios from '@/utils/request';
import {Response} from '@/utils/requestTypes.ts';

const prefix = '/wiki_project';

export const HOME_WIKI_PROJECT_CODE = 'HOME_PROJECT';

export interface WikiProjectDetail {
    id: string;
    code: string;
    name: string;
    desc: string | null;
    seq: number;
    createdAt: string | null;
    updatedAt: string | null;
}

export interface PublicWikiProjectDetail extends WikiProjectDetail {
    wikiCount: number;
    latestUpdatedAt: string | null;
}

export interface WikiProjectListResponse extends Response {
    data: WikiProjectDetail[];
}

export interface WikiProjectPageParams {
    pageIndex: number;
    pageSize: number;
    search: string | null;
}

export interface WikiProjectPageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: WikiProjectDetail[];
    };
}

export interface PublicWikiProjectPageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: PublicWikiProjectDetail[];
    };
}

export interface WikiProjectDetailResponse extends Response {
    data: WikiProjectDetail;
}

export interface EditWikiProjectParams {
    projectId: string | null;
    code: string;
    name: string;
    desc: string | null;
    seq: number;
}

export interface EditWikiProjectResponse extends Response {
    data: string;
}

export interface DeleteWikiProjectParams {
    projectId: string;
}

export const apiGetWikiProjectHome = (): Promise<WikiProjectDetailResponse> => {
    return axios.get(`${prefix}/home`);
};

export const apiGetWikiProjectDetail = (projectId: string): Promise<WikiProjectDetailResponse> => {
    return axios.get(`${prefix}/detail/${projectId}`);
};

export const apiGetPublicWikiProjectDetail = (projectId: string): Promise<WikiProjectDetailResponse> => {
    return axios.get(`${prefix}/public/detail/${projectId}`);
};

export const apiGetWikiProjectList = (): Promise<WikiProjectListResponse> => {
    return axios.get(`${prefix}/list`);
};

export const apiGetWikiProjectPage = (params: WikiProjectPageParams): Promise<WikiProjectPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export const apiGetPublicWikiProjectPage = (params: WikiProjectPageParams): Promise<PublicWikiProjectPageResponse> => {
    return axios.get(`${prefix}/public/page`, {
        params,
    });
};

export const apiEditWikiProject = (params: EditWikiProjectParams): Promise<EditWikiProjectResponse> => {
    return axios.post(`${prefix}/edit`, params);
};

export const apiDeleteWikiProject = (params: DeleteWikiProjectParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};
