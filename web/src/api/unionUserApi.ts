import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";
import {WebUserLoginDetail} from "@/api/webUserApi.ts";


const prefix = '/union_user';


export const apiUnionUserLogout = (): Promise<Response> => {
    return axios.post(`${prefix}/logout`, {});
};

export interface DeleteUnionUserParams {
    unionUserId: string;
}

export const apiDeleteUnionUser = (params: DeleteUnionUserParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};

export interface UnionUserAuthCodeLoginParams {
    authCode: string;
}

export interface UnionUserAuthCodeLoginResponse extends Response {
    data: WebUserLoginDetail
}

export const apiUnionUserAuthCodeLogin = (params: UnionUserAuthCodeLoginParams): Promise<UnionUserAuthCodeLoginResponse> => {
    return axios.post(`${prefix}/auth_code_login`, params);
};

export interface UnionUserPageParams {
    pageSize: number;
    pageIndex: number;
    search: string | null;
    searchFields?: string[];
}

export interface UnionUserDetail {
    id: string;
    name: string | null;
    enabled: boolean | null;
}

export interface UnionUserPageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: UnionUserDetail[];
    }
}

export const apiGetUnionUserPage = (params: UnionUserPageParams): Promise<UnionUserPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};
