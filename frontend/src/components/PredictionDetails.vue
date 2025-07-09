<template>
  <div>
    <h2 class="text-lg font-semibold mb-2">Prediction</h2>
    <table class="min-w-full text-sm text-center border">
      <thead class="bg-gray-100">
        <tr>
          <th class="py-2 px-3 border">Model</th>
          <th class="py-2 px-3 border">% Change (10d)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(m, name) in predictions" :key="name" class="even:bg-gray-50">
          <td class="py-2 px-3 border font-medium">{{ name }}</td>
          <td class="py-2 px-3 border">{{ m.prediction.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const predictions = ref({})
const plotUrl = ref('')
const featureImportanceUrl = ref('')


async function updatePrediction() {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/predict`)
  const data = await res.json()
  return setPredictionData(data)
}

function setPredictionData(data) {
  if (!data || data.error) {
    predictions.value = {}
    plotUrl.value = ''
    featureImportanceUrl.value = ''
    if (data && data.error) alert(`Prediction failed: ${data.error}`)
    return {
      plotUrl: '',
      featureImportanceUrl: '',
      metrics: {}
    }
  }

  predictions.value = data
  const baseline = data.baseline || {}
  plotUrl.value = baseline.plot_base64 ? `data:image/png;base64,${baseline.plot_base64}` : ''
  featureImportanceUrl.value = baseline.importance_plot_base64 ? `data:image/png;base64,${baseline.importance_plot_base64}` : ''

  return {
    plotUrl: plotUrl.value,
    featureImportanceUrl: featureImportanceUrl.value,
    metrics: data
  }
}

defineExpose({ updatePrediction, setPredictionData, plotUrl, featureImportanceUrl, predictions })
</script>

<style scoped></style>
