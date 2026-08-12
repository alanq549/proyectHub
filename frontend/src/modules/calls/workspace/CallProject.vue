<template>
  <section class="tw-space-y-6">

    <!-- =========================================================
         HEADER
    ========================================================== -->
    <div class="tw-flex tw-flex-col tw-gap-4 sm:tw-flex-row sm:tw-items-center sm:tw-justify-between">
      <div>
        <div class="tw-flex tw-items-center tw-gap-3">
          <div class="tw-flex tw-h-10 tw-w-10 tw-items-center tw-justify-center tw-rounded-xl tw-bg-primary/10">
            <span class="material-symbols-outlined notranslate tw-text-primary">
              folder_special
            </span>
          </div>

          <div>
            <h2 class="tw-text-xl tw-font-bold tw-text-on-surface">
              Proyecto Postulado
            </h2>

            <p class="tw-mt-0.5 tw-text-xs tw-text-on-surface-variant">
              Gestiona la propuesta con la que participas en
              <span class="tw-font-semibold tw-text-on-surface">
                {{ call.title }}
              </span>
            </p>
          </div>
        </div>
      </div>

      <!-- Estado de carga -->
      <div v-if="loading"
        class="tw-flex tw-items-center tw-gap-2 tw-rounded-full tw-bg-surface-container-low tw-px-3 tw-py-1.5 tw-text-xs tw-font-medium tw-text-on-surface-variant">
        <span class="material-symbols-outlined notranslate tw-animate-spin tw-text-base tw-text-primary">
          progress_activity
        </span>
        Cargando proyecto...
      </div>
    </div>


    <!-- =========================================================
         LOADING
    ========================================================== -->
    <div v-if="loading"
      class="tw-flex tw-min-h-[280px] tw-flex-col tw-items-center tw-justify-center tw-rounded-2xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest">
      <div class="tw-flex tw-h-14 tw-w-14 tw-items-center tw-justify-center tw-rounded-2xl tw-bg-primary/10">
        <span class="material-symbols-outlined notranslate tw-animate-spin tw-text-2xl tw-text-primary">
          progress_activity
        </span>
      </div>

      <p class="tw-mt-4 tw-text-sm tw-font-medium tw-text-on-surface">
        Cargando información
      </p>

      <p class="tw-mt-1 tw-text-xs tw-text-on-surface-variant">
        Estamos obteniendo los datos de tu proyecto...
      </p>
    </div>


    <!-- =========================================================
         PROYECTO VINCULADO
    ========================================================== -->
    <div v-else-if="project" class="tw-space-y-6">

      <!-- =======================================================
           PROJECT HERO
      ======================================================== -->
      <AppCard padding="md" variant="glass" class="tw-overflow-hidden">
        <div
          class="tw-relative tw-rounded-xl tw-bg-gradient-to-br tw-from-primary/10 tw-via-surface-container-low tw-to-transparent tw-p-5">

          <!-- Decorative icon -->
          <div class="tw-pointer-events-none tw-absolute tw-right-5 tw-top-4 tw-opacity-10">
            <span class="material-symbols-outlined tw-text-7xl">
              folder_special
            </span>
          </div>

          <div class="tw-relative tw-space-y-5">

            <!-- Project top -->
            <div class="tw-flex tw-flex-col tw-gap-4 sm:tw-flex-row sm:tw-items-start sm:tw-justify-between">
              <div class="tw-min-w-0">
                <div class="tw-mb-2 tw-flex tw-flex-wrap tw-items-center tw-gap-2">

                  <AppBadge :variant="getStatusVariant(project.status)">
                    {{ project.status || 'draft' }}
                  </AppBadge>

                  <span
                    class="tw-flex tw-items-center tw-gap-1.5 tw-text-[11px] tw-font-medium tw-text-on-surface-variant">
                    <span class="tw-h-1.5 tw-w-1.5 tw-rounded-full tw-bg-emerald-500"></span>
                    Proyecto vinculado
                  </span>
                </div>

                <h3 class="tw-break-words tw-text-xl tw-font-bold tw-leading-tight tw-text-on-surface">
                  {{ project.title }}
                </h3>

                <p class="tw-mt-2 tw-max-w-3xl tw-text-sm tw-leading-6 tw-text-on-surface-variant">
                  {{ project.description || 'Sin descripción provista.' }}
                </p>
              </div>

              <!-- Edit button -->
              <button v-if="project.status === 'draft'" type="button" @click="isEditing = !isEditing"
                class="tw-inline-flex tw-shrink-0 tw-items-center tw-justify-center tw-gap-2 tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3 tw-py-2 tw-text-xs tw-font-bold tw-text-on-surface tw-shadow-sm tw-transition-all hover:tw-bg-surface-container hover:tw-shadow">
                <span class="material-symbols-outlined notranslate tw-text-base">
                  {{ isEditing ? 'close' : 'edit' }}
                </span>

                {{ isEditing ? 'Cancelar' : 'Editar proyecto' }}
              </button>
            </div>


            <!-- Project metadata -->
            <div class="tw-flex tw-flex-wrap tw-gap-3 tw-border-t tw-border-outline-variant/60 tw-pt-4">
              <div
                class="tw-flex tw-items-center tw-gap-2 tw-rounded-lg tw-bg-surface-container-lowest tw-px-3 tw-py-2">
                <span class="material-symbols-outlined notranslate tw-text-base tw-text-primary">
                  category
                </span>

                <div>
                  <p class="tw-text-[10px] tw-font-medium tw-uppercase tw-tracking-wide tw-text-on-surface-variant">
                    Categoría
                  </p>

                  <p class="tw-text-xs tw-font-semibold tw-text-on-surface">
                    {{ project.category || 'Sin categoría' }}
                  </p>
                </div>
              </div>

              <div
                class="tw-flex tw-items-center tw-gap-2 tw-rounded-lg tw-bg-surface-container-lowest tw-px-3 tw-py-2">
                <span class="material-symbols-outlined notranslate tw-text-base tw-text-primary">
                  event
                </span>

                <div>
                  <p class="tw-text-[10px] tw-font-medium tw-uppercase tw-tracking-wide tw-text-on-surface-variant">
                    Estado
                  </p>

                  <p class="tw-text-xs tw-font-semibold tw-text-on-surface">
                    {{
                      project.status === 'submitted'
                        ? 'En revisión'
                        : project.status === 'approved'
                          ? 'Aprobado'
                          : project.status === 'rejected'
                            ? 'Rechazado'
                            : 'Borrador'
                    }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>


        <!-- Submit proposal -->
        <div v-if="project.status === 'draft'"
          class="tw-mt-4 tw-flex tw-flex-col tw-gap-4 tw-rounded-xl tw-border tw-border-primary/15 tw-bg-primary/5 tw-p-4 sm:tw-flex-row sm:tw-items-center sm:tw-justify-between">
          <div class="tw-flex tw-items-start tw-gap-3">
            <div
              class="tw-flex tw-h-9 tw-w-9 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-lg tw-bg-primary/10">
              <span class="material-symbols-outlined notranslate tw-text-lg tw-text-primary">
                send
              </span>
            </div>

            <div>
              <h4 class="tw-text-sm tw-font-bold tw-text-on-surface">
                ¿Todo listo con tu propuesta?
              </h4>

              <p class="tw-mt-1 tw-max-w-xl tw-text-xs tw-leading-5 tw-text-on-surface-variant">
                Envía tu proyecto a revisión. Después del envío no podrás
                modificar los documentos asociados.
              </p>
            </div>
          </div>

          <button type="button" @click="handleSubmitProposal" :disabled="saving"
            class="app-btn-primary tw-inline-flex tw-shrink-0 tw-items-center tw-justify-center tw-gap-2 tw-px-5 tw-text-sm"
            style="height: 40px;">
            <span v-if="saving" class="material-symbols-outlined notranslate tw-animate-spin tw-text-[18px]">
              progress_activity
            </span>

            <span v-else class="material-symbols-outlined notranslate tw-text-[18px]">
              send
            </span>

            {{ saving ? 'Enviando...' : 'Enviar propuesta' }}
          </button>
        </div>


        <!-- Feedback -->
        <div v-if="project.feedback"
          class="tw-mt-4 tw-rounded-xl tw-border tw-border-amber-200 tw-bg-amber-50/60 tw-p-4">
          <div class="tw-flex tw-items-start tw-gap-3">
            <div
              class="tw-flex tw-h-9 tw-w-9 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-lg tw-bg-amber-100">
              <span class="material-symbols-outlined notranslate tw-text-lg tw-text-amber-600">
                rate_review
              </span>
            </div>

            <div>
              <p class="tw-text-[11px] tw-font-bold tw-uppercase tw-tracking-wider tw-text-amber-700">
                Retroalimentación del evaluador
              </p>

              <p class="tw-mt-1 tw-text-sm tw-leading-6 tw-text-on-surface">
                {{ project.feedback }}
              </p>
            </div>
          </div>
        </div>
      </AppCard>


      <!-- =======================================================
           EDIT FORM
      ======================================================== -->
      <AppCard v-if="isEditing" padding="md" variant="glass">
        <div class="tw-mb-5 tw-flex tw-items-center tw-gap-3">
          <div class="tw-flex tw-h-9 tw-w-9 tw-items-center tw-justify-center tw-rounded-lg tw-bg-primary/10">
            <span class="material-symbols-outlined notranslate tw-text-lg tw-text-primary">
              edit_note
            </span>
          </div>

          <div>
            <h4 class="tw-text-sm tw-font-bold tw-text-on-surface">
              Editar proyecto
            </h4>

            <p class="tw-text-xs tw-text-on-surface-variant">
              Actualiza la información de tu propuesta.
            </p>
          </div>
        </div>

        <form @submit.prevent="handleUpdateProject" class="tw-space-y-5">
          <div>
            <label class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface">
              Título del Proyecto *
            </label>

            <input v-model="editForm.title" type="text" required
              class="tw-w-full tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3.5 tw-py-2.5 tw-text-sm tw-text-on-surface tw-outline-none tw-transition-all focus:tw-border-primary focus:tw-ring-2 focus:tw-ring-primary/10" />
          </div>

          <div>
            <label class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface">
              Categoría del Proyecto
            </label>

            <input v-model="editForm.category" type="text"
              class="tw-w-full tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3.5 tw-py-2.5 tw-text-sm tw-text-on-surface tw-outline-none tw-transition-all focus:tw-border-primary focus:tw-ring-2 focus:tw-ring-primary/10" />
          </div>

          <div>
            <label class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface">
              Descripción del Proyecto
            </label>

            <textarea v-model="editForm.description" rows="4"
              class="tw-w-full tw-resize-none tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-3.5 tw-text-sm tw-leading-6 tw-text-on-surface tw-outline-none tw-transition-all focus:tw-border-primary focus:tw-ring-2 focus:tw-ring-primary/10"></textarea>
          </div>

          <div class="tw-flex tw-justify-end tw-border-t tw-border-outline-variant/60 tw-pt-4">
            <button type="submit" :disabled="saving"
              class="app-btn-primary tw-inline-flex tw-items-center tw-justify-center tw-gap-2 tw-px-6 tw-text-sm"
              style="height: 40px;">
              <span v-if="saving" class="material-symbols-outlined notranslate tw-animate-spin tw-text-base">
                progress_activity
              </span>

              <span v-else class="material-symbols-outlined notranslate tw-text-base">
                save
              </span>

              {{ saving ? 'Guardando...' : 'Guardar cambios' }}
            </button>
          </div>
        </form>
      </AppCard>


      <!-- =======================================================
           DOCUMENTS
      ======================================================== -->
      <AppCard padding="md" variant="glass">
        <div class="tw-mb-5 tw-flex tw-flex-col tw-gap-4 sm:tw-flex-row sm:tw-items-center sm:tw-justify-between">
          <div class="tw-flex tw-items-center tw-gap-3">
            <div class="tw-flex tw-h-10 tw-w-10 tw-items-center tw-justify-center tw-rounded-xl tw-bg-primary/10">
              <span class="material-symbols-outlined notranslate tw-text-primary">
                folder
              </span>
            </div>

            <div>
              <div class="tw-flex tw-items-center tw-gap-2">
                <h4 class="tw-text-base tw-font-bold tw-text-on-surface">
                  Documentos del proyecto
                </h4>

                <span
                  class="tw-rounded-full tw-bg-surface-container tw-px-2 tw-py-0.5 tw-text-[10px] tw-font-bold tw-text-on-surface-variant">
                  {{ projectDocuments.length }}
                </span>
              </div>

              <p class="tw-mt-0.5 tw-text-xs tw-text-on-surface-variant">
                Requisitos técnicos y administrativos de tu propuesta.
              </p>
            </div>
          </div>

          <div>
            <input ref="fileInput" type="file" class="tw-hidden" @change="handleFileUpload" />

            <button type="button" @click="fileInput?.click()" :disabled="uploadingDoc || project.status !== 'draft'"
              class="app-btn-secondary tw-inline-flex tw-w-full tw-items-center tw-justify-center tw-gap-2 tw-px-4 tw-text-xs sm:tw-w-auto"
              style="height: 38px;">
              <span v-if="uploadingDoc" class="material-symbols-outlined notranslate tw-animate-spin tw-text-base">
                progress_activity
              </span>

              <span v-else class="material-symbols-outlined notranslate tw-text-base">
                upload_file
              </span>

              {{ uploadingDoc ? 'Subiendo...' : 'Subir archivo' }}
            </button>
          </div>
        </div>


        <!-- Documents empty state -->
        <div v-if="projectDocuments.length === 0"
          class="tw-rounded-2xl tw-border-2 tw-border-dashed tw-border-outline-variant tw-bg-surface-container-lowest tw-px-6 tw-py-12 tw-text-center">
          <div
            class="tw-mx-auto tw-flex tw-h-14 tw-w-14 tw-items-center tw-justify-center tw-rounded-2xl tw-bg-surface-container">
            <span class="material-symbols-outlined notranslate tw-text-2xl tw-text-secondary">
              folder_off
            </span>
          </div>

          <h4 class="tw-mt-4 tw-text-sm tw-font-bold tw-text-on-surface">
            No hay documentos
          </h4>

          <p class="tw-mx-auto tw-mt-1 tw-max-w-sm tw-text-xs tw-leading-5 tw-text-on-surface-variant">
            Aún no has adjuntado archivos a este proyecto.
            Sube los documentos requeridos para completar tu propuesta.
          </p>

          <button v-if="project.status === 'draft'" type="button" @click="fileInput?.click()"
            class="tw-mt-4 tw-inline-flex tw-items-center tw-gap-1.5 tw-text-xs tw-font-bold tw-text-primary hover:tw-underline">
            <span class="material-symbols-outlined notranslate tw-text-sm">
              upload
            </span>
            Subir primer documento
          </button>
        </div>


        <!-- Documents list -->
        <div v-else class="tw-space-y-2">
          <div v-for="doc in projectDocuments" :key="doc.id"
            class="tw-group tw-flex tw-items-center tw-justify-between tw-gap-4 tw-rounded-xl tw-border tw-border-outline-variant/70 tw-bg-surface-container-lowest tw-p-3.5 tw-transition-all hover:tw-border-primary/30 hover:tw-bg-surface-container-low hover:tw-shadow-sm">
            <div class="tw-flex tw-min-w-0 tw-items-center tw-gap-3">
              <div
                class="tw-flex tw-h-10 tw-w-10 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-lg tw-bg-primary/10 tw-text-primary tw-transition-colors group-hover:tw-bg-primary group-hover:tw-text-white">
                <span class="material-symbols-outlined notranslate tw-text-xl">
                  description
                </span>
              </div>

              <div class="tw-min-w-0">
                <p class="tw-truncate tw-text-sm tw-font-semibold tw-text-on-surface">
                  {{ doc.original_filename || doc.filename }}
                </p>

                <div
                  class="tw-mt-0.5 tw-flex tw-flex-wrap tw-items-center tw-gap-x-2 tw-gap-y-0.5 tw-text-[11px] tw-text-on-surface-variant">
                  <span>
                    {{ (doc.file_size / 1024).toFixed(1) }} KB
                  </span>

                  <span class="tw-text-outline">•</span>

                  <span>
                    {{ new Date(doc.created_at).toLocaleDateString('es-MX') }}
                  </span>
                </div>
              </div>
            </div>

            <div class="tw-flex tw-shrink-0 tw-items-center tw-gap-1">
              <button type="button" @click="handleDownloadDocument(doc)"
                class="tw-flex tw-h-9 tw-w-9 tw-items-center tw-justify-center tw-rounded-lg tw-text-on-surface-variant tw-transition-colors hover:tw-bg-primary/10 hover:tw-text-primary"
                title="Descargar">
                <span class="material-symbols-outlined notranslate tw-text-[19px]">
                  download
                </span>
              </button>

              <button v-if="project.status === 'draft'" type="button" @click="handleDeleteDocument(doc.id)"
                class="tw-flex tw-h-9 tw-w-9 tw-items-center tw-justify-center tw-rounded-lg tw-text-on-surface-variant tw-transition-colors hover:tw-bg-error/10 hover:tw-text-error"
                title="Eliminar">
                <span class="material-symbols-outlined notranslate tw-text-[19px]">
                  delete
                </span>
              </button>
            </div>
          </div>
        </div>
      </AppCard>
    </div>


    <!-- =========================================================
         NO PROJECT
    ========================================================== -->
    <div v-else class="tw-space-y-5">

      <!-- Intro -->
      <div
        class="tw-rounded-2xl tw-border tw-border-outline-variant tw-bg-gradient-to-br tw-from-primary/5 tw-to-transparent tw-p-5">
        <div class="tw-flex tw-items-start tw-gap-4">
          <div
            class="tw-flex tw-h-11 tw-w-11 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-xl tw-bg-primary/10">
            <span class="material-symbols-outlined notranslate tw-text-primary">
              folder_shared
            </span>
          </div>

          <div>
            <h3 class="tw-text-base tw-font-bold tw-text-on-surface">
              Vincula un proyecto a esta convocatoria
            </h3>

            <p class="tw-mt-1 tw-max-w-2xl tw-text-sm tw-leading-6 tw-text-on-surface-variant">
              Puedes seleccionar uno de tus proyectos existentes o registrar
              una nueva propuesta para participar en esta convocatoria.
            </p>
          </div>
        </div>
      </div>


      <!-- Mode selector -->
      <div class="tw-flex tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-low tw-p-1">
        <button type="button" @click="mode = 'select'"
          class="tw-flex tw-flex-1 tw-items-center tw-justify-center tw-gap-2 tw-rounded-lg tw-px-4 tw-py-2.5 tw-text-xs tw-font-bold tw-transition-all"
          :class="mode === 'select'
              ? 'tw-bg-surface-container-lowest tw-text-primary tw-shadow-sm'
              : 'tw-text-on-surface-variant hover:tw-text-on-surface'
            ">
          <span class="material-symbols-outlined notranslate tw-text-base">
            folder_open
          </span>

          Proyecto existente
        </button>

        <button type="button" @click="mode = 'create'"
          class="tw-flex tw-flex-1 tw-items-center tw-justify-center tw-gap-2 tw-rounded-lg tw-px-4 tw-py-2.5 tw-text-xs tw-font-bold tw-transition-all"
          :class="mode === 'create'
              ? 'tw-bg-surface-container-lowest tw-text-primary tw-shadow-sm'
              : 'tw-text-on-surface-variant hover:tw-text-on-surface'
            ">
          <span class="material-symbols-outlined notranslate tw-text-base">
            add_box
          </span>

          Nuevo proyecto
        </button>
      </div>


      <!-- =======================================================
           SELECT EXISTING
      ======================================================== -->
      <AppCard v-if="mode === 'select'" padding="md" variant="glass">
        <div class="tw-mb-5">
          <h3 class="tw-text-base tw-font-bold tw-text-on-surface">
            Selecciona un proyecto
          </h3>

          <p class="tw-mt-1 tw-text-xs tw-text-on-surface-variant">
            Elige una propuesta que ya tengas registrada.
          </p>
        </div>

        <div v-if="userProjects.length === 0"
          class="tw-rounded-xl tw-border tw-border-dashed tw-border-outline-variant tw-bg-surface-container-lowest tw-px-5 tw-py-10 tw-text-center">
          <span class="material-symbols-outlined notranslate tw-text-3xl tw-text-outline">
            folder_off
          </span>

          <p class="tw-mt-3 tw-text-sm tw-font-semibold tw-text-on-surface">
            No tienes proyectos registrados
          </p>

          <p class="tw-mt-1 tw-text-xs tw-text-on-surface-variant">
            Crea un nuevo proyecto para comenzar tu postulación.
          </p>

          <button type="button" @click="mode = 'create'"
            class="tw-mt-4 tw-inline-flex tw-items-center tw-gap-1.5 tw-text-xs tw-font-bold tw-text-primary hover:tw-underline">
            <span class="material-symbols-outlined notranslate tw-text-sm">
              add
            </span>
            Crear proyecto
          </button>
        </div>

        <form v-else @submit.prevent="handleLinkExistingProject" class="tw-space-y-5">
          <div>
            <label class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface">
              Proyecto a vincular
            </label>

            <select v-model="selectedProjectId" required
              class="tw-w-full tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-3 tw-text-sm tw-text-on-surface tw-outline-none tw-transition-all focus:tw-border-primary focus:tw-ring-2 focus:tw-ring-primary/10">
              <option :value="null" disabled>
                Selecciona un proyecto...
              </option>

              <option v-for="p in userProjects" :key="p.id" :value="p.id">
                {{ p.title }}
              </option>
            </select>
          </div>

          <div class="tw-flex tw-justify-end">
            <button type="submit" :disabled="!selectedProjectId || saving"
              class="app-btn-primary tw-inline-flex tw-items-center tw-justify-center tw-gap-2 tw-px-6 tw-text-sm"
              style="height: 40px;">
              <span v-if="saving" class="material-symbols-outlined notranslate tw-animate-spin tw-text-base">
                progress_activity
              </span>

              <span v-else class="material-symbols-outlined notranslate tw-text-base">
                link
              </span>

              {{ saving ? 'Vinculando...' : 'Vincular proyecto' }}
            </button>
          </div>
        </form>
      </AppCard>


      <!-- =======================================================
           CREATE PROJECT
      ======================================================== -->
      <AppCard v-else padding="md" variant="glass">
        <div class="tw-mb-5 tw-flex tw-items-center tw-gap-3">
          <div class="tw-flex tw-h-10 tw-w-10 tw-items-center tw-justify-center tw-rounded-xl tw-bg-primary/10">
            <span class="material-symbols-outlined notranslate tw-text-primary">
              add_box
            </span>
          </div>

          <div>
            <h3 class="tw-text-base tw-font-bold tw-text-on-surface">
              Crear nuevo proyecto
            </h3>

            <p class="tw-mt-0.5 tw-text-xs tw-text-on-surface-variant">
              Registra una nueva propuesta para esta convocatoria.
            </p>
          </div>
        </div>

        <form @submit.prevent="handleCreateProject" class="tw-space-y-5">
          <div>
            <label class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface">
              Título del Proyecto *
            </label>

            <input v-model="createForm.title" type="text" required placeholder="Ej. Sistema de Monitoreo Agrícola"
              class="tw-w-full tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-3 tw-text-sm tw-text-on-surface tw-outline-none tw-transition-all placeholder:tw-text-outline focus:tw-border-primary focus:tw-ring-2 focus:tw-ring-primary/10" />
          </div>

          <div>
            <label class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface">
              Descripción del Proyecto
            </label>

            <textarea v-model="createForm.description" rows="5"
              placeholder="Detalla los objetivos, problemática y propuesta..."
              class="tw-w-full tw-resize-none tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-3 tw-text-sm tw-leading-6 tw-text-on-surface tw-outline-none tw-transition-all placeholder:tw-text-outline focus:tw-border-primary focus:tw-ring-2 focus:tw-ring-primary/10"></textarea>
          </div>

          <div class="tw-flex tw-items-start tw-gap-3 tw-rounded-xl tw-bg-surface-container-low tw-p-3">
            <span class="material-symbols-outlined notranslate tw-text-base tw-text-primary">
              info
            </span>

            <p class="tw-text-xs tw-leading-5 tw-text-on-surface-variant">
              El proyecto se registrará inicialmente como
              <span class="tw-font-semibold tw-text-on-surface">
                borrador
              </span>
              y podrás agregar los documentos necesarios después.
            </p>
          </div>

          <div class="tw-flex tw-justify-end">
            <button type="submit" :disabled="saving"
              class="app-btn-primary tw-inline-flex tw-items-center tw-justify-center tw-gap-2 tw-px-6 tw-text-sm"
              style="height: 40px;">
              <span v-if="saving" class="material-symbols-outlined notranslate tw-animate-spin tw-text-base">
                progress_activity
              </span>

              <span v-else class="material-symbols-outlined notranslate tw-text-base">
                add_circle
              </span>

              {{ saving ? 'Creando...' : 'Crear y vincular proyecto' }}
            </button>
          </div>
        </form>
      </AppCard>
    </div>

  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { projectService, type Project } from '@/modules/projects/services/projectService'
import type { Call } from '../services/callService'
import type { CallWorkspace } from '../services/workspaceService'
import { documentService, type DocumentModel } from '@/modules/documents/services/documentService'

const props = defineProps<{
  call: Call
  workspace: CallWorkspace | null
}>()

const project = ref<Project | null>(null)
const userProjects = ref<Project[]>([])
const projectDocuments = ref<DocumentModel[]>([])

const loading = ref(true)
const saving = ref(false)
const uploadingDoc = ref(false)
const isEditing = ref(false)
const mode = ref<'select' | 'create'>('create')
const selectedProjectId = ref<number | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const createForm = ref({
  title: '',
  description: '',
  category: '',
  status: 'draft'
})

const editForm = ref({
  title: '',
  description: '',
  category: '',
  status: 'draft'
})

async function fetchProjectDocuments(projectId: number) {
  try {
    const docs = await documentService.getDocuments({ project_id: projectId })
    projectDocuments.value = docs
  } catch (err) {
    console.error('Error al cargar documentos del proyecto:', err)
  }
}

async function fetchCallProject() {
  try {
    loading.value = true
    const allUserProjects = await projectService.getAll()
    userProjects.value = allUserProjects

    const callProjects = await projectService.getAll({ call_id: props.call.id })

    if (callProjects.length > 0) {
      const activeProject = callProjects[0] ?? null
      project.value = activeProject

      if (activeProject) {
        populateEditForm(activeProject)
        await fetchProjectDocuments(activeProject.id)
      }
    }
  } catch (err) {
    console.error('Error al cargar proyectos:', err)
  } finally {
    loading.value = false
  }
}

function populateEditForm(proj: Project) {
  editForm.value = {
    title: proj.title || '',
    description: proj.description || '',
    category: proj.category || '',
    status: proj.status || 'draft'
  }
}

async function handleSubmitProposal() {
  if (!project.value) return

  if (!confirm('¿Estás seguro de enviar tu propuesta? Una vez enviada, cambiará de estado.')) {
    return
  }

  try {
    saving.value = true

    const updated = await projectService.update(project.value.id, {
      status: 'submitted'
    })

    project.value = updated
    populateEditForm(updated)
  } catch (err) {
    console.error('Error al enviar la propuesta:', err)
  } finally {
    saving.value = false
  }
}

async function handleLinkExistingProject() {
  if (!selectedProjectId.value) return

  try {
    saving.value = true

    const updated = await projectService.update(selectedProjectId.value, {
      call_id: props.call.id
    })

    project.value = updated
    populateEditForm(updated)

    await fetchProjectDocuments(updated.id)
  } catch (err) {
    console.error('Error al vincular el proyecto:', err)
  } finally {
    saving.value = false
  }
}

async function handleCreateProject() {
  if (!createForm.value.title.trim()) return

  try {
    saving.value = true

    const newProject = await projectService.create({
      title: createForm.value.title,
      description: createForm.value.description,
      call_id: props.call.id,
      status: createForm.value.status
    })

    project.value = newProject
    populateEditForm(newProject)

    await fetchProjectDocuments(newProject.id)
  } catch (err) {
    console.error('Error al crear el proyecto:', err)
  } finally {
    saving.value = false
  }
}

async function handleUpdateProject() {
  if (!project.value) return

  try {
    saving.value = true

    const updated = await projectService.update(project.value.id, {
      title: editForm.value.title,
      description: editForm.value.description,
      status: editForm.value.status
    })

    project.value = updated
    isEditing.value = false
  } catch (err) {
    console.error('Error al actualizar el proyecto:', err)
  } finally {
    saving.value = false
  }
}

async function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (!file || !project.value) return

  const formData = new FormData()

  formData.append('file', file)
  formData.append('project_id', project.value.id.toString())
  formData.append('call_id', props.call.id.toString())

  try {
    uploadingDoc.value = true

    await documentService.uploadDocument(formData)
    await fetchProjectDocuments(project.value.id)
  } catch (err) {
    console.error('Error al subir documento:', err)
  } finally {
    uploadingDoc.value = false

    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}

async function handleDownloadDocument(doc: DocumentModel) {
  try {
    await documentService.downloadDocument(
      doc.id,
      doc.original_filename || doc.filename
    )
  } catch (err) {
    console.error('Error al descargar archivo:', err)
  }
}

async function handleDeleteDocument(docId: number) {
  if (!confirm('¿Deseas eliminar este documento del proyecto?')) return

  try {
    await documentService.deleteDocument(docId)

    if (project.value) {
      await fetchProjectDocuments(project.value.id)
    }
  } catch (err) {
    console.error('Error al eliminar archivo:', err)
  }
}

function getStatusVariant(status?: string) {
  switch (status) {
    case 'approved':
      return 'success'
    case 'rejected':
      return 'error'
    case 'submitted':
      return 'warning'
    default:
      return 'secondary'
  }
}

onMounted(() => {
  fetchCallProject()
})
</script>