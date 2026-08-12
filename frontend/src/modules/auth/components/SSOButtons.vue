<template>
  <!-- SOCIAL LOGIN -->
  <div class="tw-flex tw-items-center tw-gap-3 tw-my-4">
    <div class="divider-line"></div>
    <span class="divider-text">
      O CONTINUAR CON
    </span>
    <div class="divider-line"></div>
  </div>

  <div class="tw-grid tw-grid-cols-1 sm:tw-grid-cols-2 tw-gap-3">
    <div class="tw-col-span-1">
      <button class="sso-btn">
        Google
      </button>
    </div>

    <div class="tw-col-span-1">
      <button class="sso-btn">
        <span class="material-symbols-outlined notranslate">
          school
        </span>
        Institucional
      </button>
    </div>
  </div>
</template>

<style scoped>
.divider-text {
  color: var(--app-on-surface-variant, #4C6479);
  font-family: var(--app-font-mono, 'IBM Plex Mono', monospace);
  font-size: 10.5px;
  letter-spacing: 0.08em;
  white-space: nowrap;
}

.divider-line {
  height: 1px;
  flex: 1;
  background-color: var(--app-outline-variant, #DCE5EC);
}

.sso-btn {
  height: 48px;
  border: 1.5px solid var(--app-outline-variant, #DCE5EC);
  border-radius: 0.5rem;
  background-color: var(--app-surface, #ffffff);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  transition: background-color .15s ease, border-color .15s ease;
  color: var(--app-primary, #1B2E44);
  font-family: var(--app-font-family, 'IBM Plex Sans', sans-serif);
  font-size: 14px;
  font-weight: 600;
}

.sso-btn:hover {
  background-color: var(--app-accent-melon-light, #E8D2A6);
  border-color: var(--app-accent-melon, #B8863B);
  color: var(--app-ink-900, #14243A);
}

.sso-btn svg,
.sso-btn .material-symbols-outlined {
  transition: transform .15s ease;
  color: var(--app-accent-melon, #B8863B);
}

.sso-btn:hover svg,
.sso-btn:hover .material-symbols-outlined {
  transform: scale(1.1);
}
</style>
