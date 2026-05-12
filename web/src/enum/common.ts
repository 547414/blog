export enum EnumUserRoleCode {
    SUPER_ADMIN = 'SUPER_ADMIN',
    ADMIN = 'ADMIN',
    WEB_USER = 'WEB_USER',
}

export const userRoleEnum = {
    [EnumUserRoleCode.SUPER_ADMIN]: '超级管理员',
    [EnumUserRoleCode.ADMIN]: '管理员',
    [EnumUserRoleCode.WEB_USER]: 'WEB用户',
}
