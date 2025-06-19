<template>
  <div>
    <h2>Prediction Details</h2>
    <p>Predicted % change in 10 days: <strong>{{ prediction.toFixed(2) }}%</strong></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const prediction = ref(0)
const plotUrl = ref('')

async function updatePrediction() {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/predict`)
  const data = await res.json()
  
  if (data.error) {
    prediction.value = 0
    plotUrl.value = ''
    alert(`Prediction failed: ${data.error}`)
    return { plotUrl: '' }
  }
    
  prediction.value = data.prediction
  plotUrl.value = `data:image/png;base64,${data.plot_base64}`
  return { plotUrl: plotUrl.value }
}

// allow this to be triggered externally
defineExpose({ updatePrediction, plotUrl })
</script>
