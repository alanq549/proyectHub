<template>
  <div class="secure-badge">
    <span class="material-symbols-outlined">
      verified_user
    </span>
    <span class="txt">
      Encriptación de nivel bancario
    </span>
  </div>
</template>

<style scoped>
.secure-badge {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  border: 1px solid #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  z-index: 20;
}

.secure-badge .material-symbols-outlined {
  font-size: 16px;
  color: #16a34a;
  font-variation-settings: 'FILL' 1;
}

.secure-badge span.txt {
  color: var(--on-surface-variant, #45464d);
  font-size: 12px;
  font-weight: 500;
}
</style>