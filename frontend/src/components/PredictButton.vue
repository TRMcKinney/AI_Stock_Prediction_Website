<template>
  <div style="margin: 1rem 0;">
    <div class="model-options">
      <label v-for="opt in modelOptions" :key="opt.value">
        <input type="checkbox" v-model="selectedModels" :value="opt.value" />
        {{ opt.label }}
      </label>
    </div>
    <button @click="predict">Predict</button>
  </div>
</template>

<script setup>
import { inject, ref } from 'vue'
const triggerPrediction = inject('triggerPrediction')

const modelOptions = [
  { value: 'baseline', label: 'Baseline' },
  { value: 'cross_validation', label: 'Cross Validation' },
  { value: 'persist', label: 'Persisted' },
  { value: 'grid_search', label: 'Grid Search' }
]
const selectedModels = ref(modelOptions.map(o => o.value))

function predict() {
  triggerPrediction(selectedModels.value)
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
.model-options {
  margin-bottom: 0.5rem;
}
.model-options label {
  margin-right: 0.5rem;
  font-size: 0.9rem;
}
</style>
