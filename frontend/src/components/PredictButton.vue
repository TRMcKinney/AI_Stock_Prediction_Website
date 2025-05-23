<template>
  <div style="margin: 1rem 0;">
    <button @click="predict">Predict</button>
    <span style="margin-left: 0.5rem; font-size: 0.9rem; color: #b35b00;">Neural Network Model</span>
  </div>
</template>

<script setup>
import { inject } from 'vue'
const triggerPrediction = inject('triggerPrediction')

function predict() {
  // alert('Running prediction...')
  triggerPrediction()
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
