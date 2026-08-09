// src/modules/documents/routes/index.ts

import type { RouteRecordRaw } from 'vue-router'

export const documentsRoutes: RouteRecordRaw[] = [
    // ─────────────────────────────────────────────
    // Lista de documentos
    // ─────────────────────────────────────────────
    {
        path: '/documents',
        name: 'documents-list',
        component: () => import('../views/DocumentsView.vue'),
        meta: {
            requiresAuth: true
        }
    }
    
]
