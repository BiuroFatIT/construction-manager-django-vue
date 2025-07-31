import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: 'cm', 
                    name: 'constructionManager',
                    children: [
                        {
                            path: 'companies',
                            name: 'companies',
                            component: () => import('@/views/companies/containers/Companies.vue')
                        },
                        {
                            path: 'products',
                            name: 'products',
                            component: () => import('@/views/products/containers/Products.vue')
                        }
                    ]
                },
            ]
        },
        {
            path: '/landing',
            name: 'landing',
            component: () => import('@/views/general/Landing.vue')
        },
        {
            path: '/pages/notfound',
            name: 'notfound',
            component: () => import('@/views/general/NotFound.vue')
        },

        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/general/AuthLogin.vue')
        },
        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/general/AuthAccessDenied.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/general/AuthError.vue')
        }
    ]
});

export default router;
