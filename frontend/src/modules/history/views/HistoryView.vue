<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { historyService, type ActivityLogModel } from '../services/historyService'
import { useAuthStore } from '@/stores/authStore'
import AppCard from '@/shared/components/AppCard.vue'
import AppBadge from '@/shared/components/AppBadge.vue'

const authStore = useAuthStore()

const logs = ref<ActivityLogModel[]>([])
const loading = ref(true)

const isAdmin = computed(() => authStore.user?.role === 'admin')

const getActionIcon = (action?: string) => {
  const value = action?.toLowerCase() || ''

  if (value.includes('create') || value.includes('crear')) {
    return 'add_circle'
  }

  if (value.includes('update') || value.includes('edit') || value.includes('actual')) {
    return 'edit'
  }

  if (value.includes('delete') || value.includes('elimin')) {
    return 'delete'
  }

  if (value.includes('login') || value.includes('inicio')) {
    return 'login'
  }

  if (value.includes('logout') || value.includes('cierre')) {
    return 'logout'
  }

  if (value.includes('upload') || value.includes('sub')) {
    return 'upload_file'
  }

  if (value.includes('download') || value.includes('descarg')) {
    return 'download'
  }

  if (value.includes('submit') || value.includes('envi')) {
    return 'send'
  }

  return 'history'
}

function getActionVariant(action: string) {
  switch (action) {
    case 'create':
      return 'success'
    case 'update':
      return 'warning'
    case 'delete':
      return 'error'
    default:
      return 'neutral'
  }
}

const formatAction = (action?: string) => {
  if (!action) return 'Actividad'

  return action
    .replace(/_/g, ' ')
    .replace(/\b\w/g, char => char.toUpperCase())
}

const formatEntity = (log: ActivityLogModel) => {
  if (!log.entity_type) return null

  const entity = log.entity_type
    .replace(/_/g, ' ')
    .replace(/\b\w/g, char => char.toUpperCase())

  return log.entity_id
    ? `${entity} #${log.entity_id}`
    : entity
}

const formatDate = (date: string) => {
  const parsedDate = new Date(date)

  if (Number.isNaN(parsedDate.getTime())) {
    return 'Fecha desconocida'
  }

  return parsedDate.toLocaleString('es-MX', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

async function fetchHistory() {
  try {
    loading.value = true
    logs.value = await historyService.getHistory({ limit: 50 })
  } catch (err) {
    console.error('Error al cargar el historial:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHistory()
})
</script>

<template>
  <section class="tw-space-y-6">

    <!-- ========================================================= -->
    <!-- HEADER -->
    <!-- ========================================================= -->

    <div class="tw-relative">

      <div class="tw-flex tw-items-center tw-gap-2 tw-mb-2">
        <span class="tw-h-px tw-w-7 tw-bg-primary/60"></span>

        <span
          class="tw-text-[10px] tw-font-bold tw-uppercase tw-tracking-[0.2em] tw-text-primary"
        >
          {{ isAdmin ? 'Auditoría' : 'Actividad' }}
        </span>
      </div>

      <div class="tw-flex tw-items-start tw-justify-between tw-gap-4">

        <div class="tw-flex tw-items-center tw-gap-3">

          <div
            class="tw-flex tw-h-11 tw-w-11 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-xl tw-bg-primary tw-text-on-primary tw-shadow-lg"
          >
            <span class="material-symbols-outlined notranslate tw-text-2xl">
              history
            </span>
          </div>

          <div>
            <h2
              class="tw-text-2xl tw-font-bold tw-leading-tight tw-text-on-surface"
            >
              {{
                isAdmin
                  ? 'Auditoría General del Sistema'
                  : 'Mi Historial de Actividad'
              }}
            </h2>

            <p
              class="tw-mt-1 tw-text-xs tw-text-on-surface-variant"
            >
              {{
                isAdmin
                  ? 'Registro global de acciones realizadas por los usuarios en la plataforma.'
                  : 'Consulta las acciones recientes realizadas con tu cuenta.'
              }}
            </p>
          </div>

        </div>

        <!-- Contador -->
        <div
          v-if="!loading"
          class="tw-hidden sm:tw-flex tw-items-center tw-gap-2 tw-rounded-xl tw-border tw-border-outline-variant/60 tw-bg-surface-container-low tw-px-3 tw-py-2"
        >
          <span class="material-symbols-outlined notranslate tw-text-base tw-text-primary">
            list_alt
          </span>

          <span class="tw-text-xs tw-font-semibold tw-text-on-surface">
            {{ logs.length }}
          </span>

          <span class="tw-text-[10px] tw-text-on-surface-variant">
            registros
          </span>
        </div>

      </div>
    </div>


    <!-- ========================================================= -->
    <!-- LOADING -->
    <!-- ========================================================= -->

    <AppCard
      v-if="loading"
      variant="glass"
      class="tw-border tw-border-outline-variant/60"
    >
      <div class="tw-flex tw-flex-col tw-items-center tw-justify-center tw-py-14">

        <div
          class="tw-flex tw-h-12 tw-w-12 tw-items-center tw-justify-center tw-rounded-full tw-bg-primary/10"
        >
          <span
            class="material-symbols-outlined notranslate tw-animate-spin tw-text-2xl tw-text-primary"
          >
            progress_activity
          </span>
        </div>

        <p class="tw-mt-4 tw-text-sm tw-font-medium tw-text-on-surface">
          Cargando historial
        </p>

        <p class="tw-mt-1 tw-text-xs tw-text-on-surface-variant">
          Estamos recuperando los registros de actividad...
        </p>

      </div>
    </AppCard>


    <!-- ========================================================= -->
    <!-- HISTORIAL -->
    <!-- ========================================================= -->

    <AppCard
      v-else
      variant="glass"
      class="tw-relative tw-overflow-hidden tw-border tw-border-outline-variant/60 tw-bg-surface-container/80 tw-backdrop-blur-xl"
    >

      <!-- Línea decorativa -->
      <div
        class="tw-absolute tw-left-0 tw-right-0 tw-top-0 tw-h-px tw-bg-gradient-to-r tw-from-transparent tw-via-primary/50 tw-to-transparent"
      />

      <template #header>
        <div class="tw-flex tw-items-center tw-justify-between">

          <div>
            <h3 class="tw-text-sm tw-font-bold tw-text-on-surface">
              Registro de actividad
            </h3>

            <p class="tw-mt-0.5 tw-text-[11px] tw-text-on-surface-variant">
              Últimas acciones registradas en el sistema.
            </p>
          </div>

          <div
            class="tw-flex tw-items-center tw-gap-1.5 tw-rounded-lg tw-bg-surface-container tw-px-2.5 tw-py-1.5"
          >
            <span class="material-symbols-outlined notranslate tw-text-sm tw-text-primary">
              schedule
            </span>

            <span class="tw-text-[10px] tw-font-medium tw-text-on-surface-variant">
              Más recientes
            </span>
          </div>

        </div>
      </template>


      <!-- ======================================================= -->
      <!-- EMPTY STATE -->
      <!-- ======================================================= -->

      <div
        v-if="logs.length === 0"
        class="tw-flex tw-flex-col tw-items-center tw-justify-center tw-py-14"
      >

        <div
          class="tw-flex tw-h-16 tw-w-16 tw-items-center tw-justify-center tw-rounded-2xl tw-bg-surface-container tw-border tw-border-outline-variant/60"
        >
          <span
            class="material-symbols-outlined notranslate tw-text-3xl tw-text-outline"
          >
            event_busy
          </span>
        </div>

        <h3
          class="tw-mt-4 tw-text-sm tw-font-bold tw-text-on-surface"
        >
          No hay actividad registrada
        </h3>

        <p
          class="tw-mt-1 tw-max-w-sm tw-text-center tw-text-xs tw-text-on-surface-variant"
        >
          Todavía no existen registros de actividad disponibles para mostrar.
        </p>

      </div>


      <!-- ======================================================= -->
      <!-- DESKTOP TABLE -->
      <!-- ======================================================= -->

      <div
        v-else
        class="tw-hidden md:tw-block tw-overflow-x-auto"
      >

        <table class="tw-w-full tw-border-collapse">

          <thead>
            <tr
              class="tw-border-b tw-border-outline-variant/60"
            >

              <th
                v-if="isAdmin"
                class="tw-px-4 tw-pb-3 tw-text-left tw-text-[10px] tw-font-bold tw-uppercase tw-tracking-wider tw-text-on-surface-variant"
              >
                Usuario
              </th>

              <th
                class="tw-px-4 tw-pb-3 tw-text-left tw-text-[10px] tw-font-bold tw-uppercase tw-tracking-wider tw-text-on-surface-variant"
              >
                Acción
              </th>

              <th
                class="tw-px-4 tw-pb-3 tw-text-left tw-text-[10px] tw-font-bold tw-uppercase tw-tracking-wider tw-text-on-surface-variant"
              >
                Entidad
              </th>

              <th
                class="tw-px-4 tw-pb-3 tw-text-left tw-text-[10px] tw-font-bold tw-uppercase tw-tracking-wider tw-text-on-surface-variant"
              >
                Detalles
              </th>

              <th
                class="tw-px-4 tw-pb-3 tw-text-right tw-text-[10px] tw-font-bold tw-uppercase tw-tracking-wider tw-text-on-surface-variant"
              >
                Fecha
              </th>

            </tr>
          </thead>


          <tbody>

            <tr
              v-for="log in logs"
              :key="log.id"
              class="tw-group tw-border-b tw-border-outline-variant/40 last:tw-border-0 hover:tw-bg-primary/[0.035] tw-transition-colors"
            >

              <!-- Usuario -->
              <td
                v-if="isAdmin"
                class="tw-px-4 tw-py-4"
              >
                <div class="tw-flex tw-items-center tw-gap-2">

                  <div
                    class="tw-flex tw-h-8 tw-w-8 tw-items-center tw-justify-center tw-rounded-lg tw-bg-surface-container tw-border tw-border-outline-variant/60"
                  >
                    <span class="material-symbols-outlined notranslate tw-text-sm tw-text-on-surface-variant">
                      person
                    </span>
                  </div>

                  <span
                    class="tw-font-mono tw-text-[11px] tw-font-semibold tw-text-on-surface-variant"
                  >
                    #{{ log.user_id }}
                  </span>

                </div>
              </td>


              <!-- Acción -->
              <td class="tw-px-4 tw-py-4">

                <div class="tw-flex tw-items-center tw-gap-2.5">

                  <div
                    class="tw-flex tw-h-8 tw-w-8 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-lg tw-bg-primary/10 tw-text-primary"
                  >
                    <span class="material-symbols-outlined notranslate tw-text-base">
                      {{ getActionIcon(log.action) }}
                    </span>
                  </div>

                  <AppBadge
                    :variant="getActionVariant(log.action)"
                  >
                    {{ formatAction(log.action) }}
                  </AppBadge>

                </div>

              </td>


              <!-- Entidad -->
              <td class="tw-px-4 tw-py-4">

                <div
                  v-if="formatEntity(log)"
                  class="tw-inline-flex tw-items-center tw-gap-1.5 tw-rounded-lg tw-border tw-border-outline-variant/60 tw-bg-surface-container-low tw-px-2.5 tw-py-1.5"
                >
                  <span class="material-symbols-outlined notranslate tw-text-sm tw-text-on-surface-variant">
                    category
                  </span>

                  <span
                    class="tw-text-[11px] tw-font-medium tw-text-on-surface-variant"
                  >
                    {{ formatEntity(log) }}
                  </span>
                </div>

                <span
                  v-else
                  class="tw-text-xs tw-text-outline"
                >
                  Sin entidad
                </span>

              </td>


              <!-- Detalles -->
              <td
                class="tw-max-w-[340px] tw-px-4 tw-py-4"
              >

                <p
                  class="tw-truncate tw-text-xs tw-text-on-surface-variant"
                  :title="log.description || 'Sin detalles adicionales'"
                >
                  {{ log.description || 'Sin detalles adicionales' }}
                </p>

              </td>


              <!-- Fecha -->
              <td
                class="tw-whitespace-nowrap tw-px-4 tw-py-4 tw-text-right"
              >

                <div class="tw-flex tw-flex-col tw-items-end">

                  <span
                    class="tw-text-xs tw-font-medium tw-text-on-surface"
                  >
                    {{ formatDate(log.created_at).split(',')[0] }}
                  </span>

                  <span
                    class="tw-mt-0.5 tw-text-[10px] tw-text-on-surface-variant"
                  >
                    {{ formatDate(log.created_at).split(',').slice(1).join(',') }}
                  </span>

                </div>

              </td>

            </tr>

          </tbody>

        </table>

      </div>


      <!-- ======================================================= -->
      <!-- MOBILE TIMELINE -->
      <!-- ======================================================= -->

      <div
        v-if="logs.length > 0"
        class="md:tw-hidden tw-space-y-0"
      >

        <div
          v-for="(log, index) in logs"
          :key="log.id"
          class="tw-relative tw-flex tw-gap-3 tw-py-4"
        >

          <!-- Línea -->
          <div
            v-if="index < logs.length - 1"
            class="tw-absolute tw-left-[15px] tw-top-12 tw-bottom-0 tw-w-px tw-bg-outline-variant/60"
          />

          <!-- Icono -->
          <div
            class="tw-relative tw-z-10 tw-flex tw-h-8 tw-w-8 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-lg tw-bg-primary/10 tw-text-primary"
          >
            <span class="material-symbols-outlined notranslate tw-text-base">
              {{ getActionIcon(log.action) }}
            </span>
          </div>


          <div class="tw-min-w-0 tw-flex-1">

            <div
              class="tw-flex tw-flex-wrap tw-items-center tw-justify-between tw-gap-2"
            >

              <AppBadge
                :variant="getActionVariant(log.action)"
              >
                {{ formatAction(log.action) }}
              </AppBadge>

              <span
                class="tw-text-[10px] tw-text-on-surface-variant"
              >
                {{ formatDate(log.created_at) }}
              </span>

            </div>


            <!-- Usuario admin -->
            <div
              v-if="isAdmin"
              class="tw-mt-2 tw-flex tw-items-center tw-gap-1.5"
            >
              <span class="material-symbols-outlined notranslate tw-text-xs tw-text-outline">
                person
              </span>

              <span
                class="tw-font-mono tw-text-[10px] tw-text-on-surface-variant"
              >
                Usuario #{{ log.user_id }}
              </span>
            </div>


            <!-- Entidad -->
            <div
              v-if="formatEntity(log)"
              class="tw-mt-2"
            >
              <span
                class="tw-inline-flex tw-items-center tw-gap-1 tw-rounded-md tw-bg-surface-container tw-px-2 tw-py-1 tw-text-[10px] tw-font-medium tw-text-on-surface-variant"
              >
                <span class="material-symbols-outlined notranslate tw-text-xs">
                  category
                </span>

                {{ formatEntity(log) }}
              </span>
            </div>


            <!-- Descripción -->
            <p
              class="tw-mt-2 tw-text-xs tw-leading-relaxed tw-text-on-surface-variant"
            >
              {{ log.description || 'Sin detalles adicionales.' }}
            </p>

          </div>

        </div>

      </div>

    </AppCard>

  </section>
</template>