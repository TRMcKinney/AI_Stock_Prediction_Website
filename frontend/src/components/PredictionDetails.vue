<template>
  <div>
    <h2>Prediction Details</h2>
    <p>Predicted % change in 10 days: <strong>{{ prediction.toFixed(2) }}%</strong></p>
    <img :src="plotUrl" alt="Prediction scatter plot" v-if="plotUrl" />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const prediction = ref(0)
const plotUrl = ref('')

async function updatePrediction() {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/predict`)
  const data = await res.json()
  prediction.value = data.prediction
  plotUrl.value = `data:image/png;base64,${data.plot_base64}`
}

// allow this to be triggered externally
defineExpose({ updatePrediction })
</script>
