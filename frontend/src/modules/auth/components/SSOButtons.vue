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
  color: var(--outline-variant, #c6c6cd);
  font-size: 12px;
  letter-spacing: 0.03em;
  white-space: nowrap;
}

.divider-line {
  height: 1px;
  flex: 1;
  background-color: var(--outline-variant, #c6c6cd);
}

.sso-btn {
  height: 48px;
  border: 1px solid var(--outline-variant, #c6c6cd);
  border-radius: 0.75rem;
  background-color: var(--surface, #f7f9fb);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  transition: background-color .15s ease;
  color: var(--on-surface, #191c1e);
  font-size: 14px;
  font-weight: 500;
}

.sso-btn:hover {
  background-color: var(--surface-container, #eceef0);
  color: var(--on-surface, #191c1e);
}

.sso-btn svg,
.sso-btn .material-symbols-outlined {
  transition: transform .15s ease;
}

.sso-btn:hover svg,
.sso-btn:hover .material-symbols-outlined {
  transform: scale(1.1);
}
</style>
