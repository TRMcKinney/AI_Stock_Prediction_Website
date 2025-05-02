<template>
  <div style="margin: 1rem 0;">
    <button @click="predict">Predict</button>
  </div>
</template>

<script setup>
function predict() {
  alert('Prediction button clicked!')
  // Later: use axios to call FastAPI
}
</script>

<style scoped>
button {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  background-color: #410093;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #5e2db7;
}
</style>