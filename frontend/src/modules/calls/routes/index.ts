// src/modules/calls/routes/index.ts
import type { RouteRecordRaw } from 'vue-router'
import { useWorkspaceStore } from '../stores/workspaceStore'

export const callsRoutes: RouteRecordRaw[] = [
  // ─────────────────────────────────────────────
  // Lista de convocatorias
  // ─────────────────────────────────────────────
  {
    path: '/calls',
    name: 'calls-list',
    component: () => import('../views/CallsListView.vue'),
    meta: {
      requiresAuth: true
    }
  },

  // ─────────────────────────────────────────────
  // Workspace de una convocatoria
  // ─────────────────────────────────────────────
  {
    path: '/calls/:id',
    name: 'call-detail',
    component: () => import('../views/CallWorkspaceView.vue'),
    meta: {
      requiresAuth: true
    },

    children: [
      // /calls/:id  --> Redirección inteligente vía Guard de Navegación
      {
        path: '',
        name: 'call-workspace-root',
        component: { render: () => null }, // Componente Dummy para evitar error de RouteRecord
        beforeEnter: async (to) => {
          const callId = Number(to.params.id)
          if (!Number.isInteger(callId)) {
            return { name: 'calls-list' }
          }

          const workspaceStore = useWorkspaceStore()
          try {
            const workspace = await workspaceStore.fetchWorkspace(callId)
            const status = (workspace as Record<string, any>).participant_status ?? 'NOT_REGISTERED'

            if (status === 'NOT_REGISTERED') {
              return { name: 'call-information', params: { id: callId } }
            }

            return { name: 'call-project', params: { id: callId } }
          } catch {
            return { name: 'call-information', params: { id: callId } }
          }
        }
      },

      // /calls/:id/information
      {
        path: 'information',
        name: 'call-information',
        component: () => import('../workspace/CallInformation.vue'),
        meta: {
          requiresAuth: true
        }
      },

      // /calls/:id/project
      {
        path: 'project',
        name: 'call-project',
        component: () => import('../workspace/CallProject.vue'),
        meta: {
          requiresAuth: true
        }
      },
      
      {
      path: 'submissions',
      name: 'call-submissions',
      component: () => import('@/modules/calls/views/CallSubmissionsView.vue'),
      meta: { requiresAdmin: true }
    },

      // /calls/:id/documents
      {
        path: 'documents',
        name: 'call-documents',
        component: () => import('../workspace/CallDocuments.vue'),
        meta: {
          requiresAuth: true
        }
      },

      // /calls/:id/tracking
      {
        path: 'tracking',
        name: 'call-tracking',
        component: () => import('../workspace/CallTracking.vue'),
        meta: {
          requiresAuth: true
        }
      }
    ]
  }
]