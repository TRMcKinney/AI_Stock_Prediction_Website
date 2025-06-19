<template>
  <div>
    <h2>Prediction</h2>
    <p>Predicted % change in 10 days: <strong>{{ prediction.toFixed(2) }}%</strong></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const prediction = ref(0)
const plotUrl = ref('')
const featureImportanceUrl = ref('')
const r2 = ref(0)
const mae = ref(0)
const rmse = ref(0)

async function updatePrediction() {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/predict`)
  const data = await res.json()
  
  if (data.error) {
    prediction.value = 0
    plotUrl.value = ''
    featureImportanceUrl.value = ''
    r2.value = 0
    mae.value = 0
    rmse.value = 0
    alert(`Prediction failed: ${data.error}`)
    return {
      plotUrl: '',
      featureImportanceUrl: '',
      r2: 0,
      mae: 0,
      rmse: 0
    }
  }

  prediction.value = data.prediction
  plotUrl.value = `data:image/png;base64,${data.plot_base64}`
  featureImportanceUrl.value = `data:image/png;base64,${data.importance_plot_base64}`
  r2.value = data.r2
  mae.value = data.mae
  rmse.value = data.rmse
  return {
    plotUrl: plotUrl.value,
    featureImportanceUrl: featureImportanceUrl.value,
    r2: r2.value,
    mae: mae.value,
    rmse: rmse.value
  }
}

// allow this to be triggered externally
defineExpose({ updatePrediction, plotUrl, featureImportanceUrl, r2, mae, rmse })
</script>
