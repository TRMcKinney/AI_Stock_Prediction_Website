<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* ensures it's above all other elements */
  pointer-events: all;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  width: 300px;
}
</style>
