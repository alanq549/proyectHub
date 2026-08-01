<template>
  <!-- Mobile Branding -->
  <div class="d-lg-none mobile-brand">
    <div class="mobile-logo-badge">
      <span class="material-symbols-outlined" style="font-size:18px;">
        account_tree
      </span>
    </div>
    <span class="sidebar-brand-name">
      ProjectHub
    </span>
  </div>
</template>

<style scoped>
.mobile-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 3rem;
}

.mobile-logo-badge {
  width: 32px;
  height: 32px;
  background-color: var(--primary, #000000);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.sidebar-brand-name {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--primary, #000000);
}
</style>