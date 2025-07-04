<template>
  <div style="margin: 1rem 0;">
    <button class="open-btn" @click="openModal">Make a Prediction</button>

    <Modal v-if="showModal" @close="closeModal">
      <div class="model-options">
        <label v-for="opt in modelOptions" :key="opt.value" class="model-option">
          <input type="checkbox" v-model="selectedModels" :value="opt.value" />
          <span class="label">{{ opt.label }}</span>
          <div class="description">{{ opt.description }}</div>
        </label>
      </div>
      <button class="predict-btn" @click="startPrediction">Predict</button>
    </Modal>
  </div>
</template>

<script setup>
import { inject, ref } from 'vue'
import Modal from './Modal.vue'

const triggerPrediction = inject('triggerPrediction')

const modelOptions = [
  {
    value: 'baseline',
    label: 'Baseline',
    description:
      'Trains a lightweight neural network on recent data to forecast the next 10 days.',
  },
  {
    value: 'cross_validation',
    label: 'Cross Validation',
    description:
      'Evaluates the model with time-series cross validation and averages the metrics.',
  },
  {
    value: 'persist',
    label: 'Persisted',
    description:
      'Loads a previously saved model from Supabase if available and reuses it.',
  },
  {
    value: 'grid_search',
    label: 'Grid Search',
    description:
      'Runs a small grid search over network parameters and picks the best performer.',
  },
]

const selectedModels = ref(modelOptions.map((o) => o.value))
const showModal = ref(false)

function openModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

function startPrediction() {
  showModal.value = false
  triggerPrediction(selectedModels.value)
}
</script>

<style scoped>
.open-btn,
.predict-btn {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  background-color: #410093;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.open-btn:hover,
.predict-btn:hover {
  background-color: #5e2db7;
}
.model-options {
  margin-bottom: 0.5rem;
}
.model-option {
  display: block;
  margin-bottom: 0.75rem;
  text-align: left;
}
.label {
  margin-left: 0.25rem;
  font-weight: 600;
}
.description {
  font-size: 0.85rem;
  margin-left: 1.5rem;
  margin-top: 0.25rem;
  color: #555;
}
.predict-btn {
  display: block;
  margin: 0.5rem auto 0;
}
</style>
