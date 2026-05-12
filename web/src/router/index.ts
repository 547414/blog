// src/router/index.ts
import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import BlankLayout from "@/layouts/BlankLayout.vue";

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        component: BlankLayout,
        children: [
            {
                path: '',
                name: 'Home',
                component: () => import('@/views/Home.vue'),
                meta: {
                    needAuth: false,
                    alias: '首页',
                    key: 'HOME',
                    pathList: ['/'],
                    pathAliasList: ['首页']
                }
            },
        ],

    },
    {
        path: '/public-wiki/:projectId',
        component: BlankLayout,
        children: [
            {
                path: '',
                name: 'PublicWiki',
                component: () => import('@/views/Home.vue'),
                meta: {
                    needAuth: false,
                    alias: '公开Wiki',
                    key: 'PUBLIC_WIKI',
                    pathList: ['/public-wiki'],
                    pathAliasList: ['公开Wiki']
                }
            },
        ],
    },
    {
        path: '/auth',
        component: BlankLayout,
        children: [
            {
                path: '/login',
                name: 'Login',
                component: () => import('@/views/auth/Login.vue'),
                meta: {
                    needAuth: false,
                    alias: '登录',
                    key: 'LOGIN',
                    pathList: ['/login'],
                    pathAliasList: ['登录']
                }
            },
            {
                path: '/register',
                name: 'Register',
                component: () => import('@/views/auth/Register.vue'),
                meta: {
                    needAuth: false,
                    alias: '注册',
                    key: 'REGISTER',
                    pathList: ['/register'],
                    pathAliasList: ['注册']
                }
            }
        ]
    },
    {
        path: '/sys',
        component: DefaultLayout,
        children: [
            {
                path: '/sys/role',
                name: 'Role',
                component: () => import('@/views/sys/role/Index.vue'),
                meta: {
                    needAuth: true,
                    alias: '角色管理',
                    key: 'ROLE',
                    pathList: ['/sys/role'],
                    pathAliasList: ['角色管理']
                }
            },
            {
                path: '/sys/menu',
                name: 'Menu',
                component: () => import('@/views/sys/menu/Index.vue'),
                meta: {
                    needAuth: true,
                    alias: '菜单管理',
                    key: 'MENU',
                    pathList: ['/sys/menu'],
                    pathAliasList: ['菜单管理']
                }
            },
            {
                path: '/sys/permission',
                name: 'Permission',
                component: () => import('@/views/sys/permission/Index.vue'),
                meta: {
                    needAuth: true,
                    alias: '功能权限',
                    key: 'PERMISSION',
                    pathList: ['/sys/permission'],
                    pathAliasList: ['功能权限']
                }
            },
            {
                path: '/sys/people',
                name: 'People',
                component: () => import('@/views/sys/people/Index.vue'),
                meta: {
                    needAuth: true,
                    alias: '人员管理',
                    key: 'PEOPLE',
                    pathList: ['/sys/people'],
                    pathAliasList: ['人员管理']
                }
            },
            {
                path: '/sys/organization',
                name: 'Organization',
                component: () => import('@/views/sys/organization/Index.vue'),
                meta: {
                    needAuth: true,
                    alias: '组织管理',
                    key: 'ORGANIZATION',
                    pathList: ['/sys/organization'],
                    pathAliasList: ['组织管理']
                }
            },
            {
                path: '/sys/dept',
                name: 'Dept',
                component: () => import('@/views/sys/dept/Index.vue'),
                meta: {
                    needAuth: true,
                    alias: '部门管理',
                    key: 'DEPT',
                    pathList: ['/sys/dept'],
                    pathAliasList: ['部门管理']
                }
            },
            {
                path: '/sys/invite',
                name: 'Invite',
                component: () => import('@/views/sys/invite/Index.vue'),
                meta: {
                    needAuth: true,
                    alias: '邀请码管理',
                    key: 'INVITE',
                    pathList: ['/sys/invite'],
                    pathAliasList: ['部门管理']
                }
            },
        ]
    },
    {
        path: '/wiki',
        component: DefaultLayout,
        children: [
            {
                path: '/wiki-project',
                name: 'WikiProject',
                component: () => import('@/views/wiki/ProjectIndex.vue'),
                meta: {
                    needAuth: true,
                    alias: 'Wiki项目',
                    key: 'WIKI_PROJECT',
                    pathList: ['/wiki-project'],
                    pathAliasList: ['Wiki项目']
                }
            },
            {
                path: '',
                name: 'Wiki',
                component: () => import('@/views/wiki/Index.vue'),
                meta: {
                    needAuth: true,
                    alias: 'Wiki管理',
                    key: 'WIKI',
                    pathList: ['/wiki'],
                    pathAliasList: ['Wiki管理']
                }
            }
        ]
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

router.beforeEach((_to, _from, next) => {
    next()
})

export default router
