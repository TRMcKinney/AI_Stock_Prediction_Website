<template>
  <section id="why-trust" ref="sectionRef" class="py-20 bg-white text-center" v-motion="{ initial: { opacity: 0, y: 50 }, visibleOnce: { opacity: 1, y: 0 } }">
    <h2 class="text-3xl font-bold mb-6 text-gray-900">Why Trust It?</h2>
    <p class="max-w-3xl mx-auto mb-6 text-gray-700">
      Our predictions are powered by an LSTM neural network trained on years of Apple stock data.
    </p>
    <div class="max-w-xl mx-auto h-64 mb-6">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    <div class="max-w-xl mx-auto">
      <button @click="showInfo = !showInfo" class="px-4 py-2 rounded bg-gray-200">
        {{ showInfo ? 'Hide' : 'View' }} model training info
      </button>
      <div v-if="showInfo" class="mt-4 text-left p-4 bg-gray-100 rounded">
        <p class="text-sm text-gray-600">
          The model uses a multi-layer LSTM with dropout and is trained on daily prices from the past decade. Metrics such as MAE and RMSE are tracked during training.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale)
const chartData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [{
    label: 'Prediction Accuracy (%)',
    data: [60, 65, 70, 75, 80, 82],
    fill: false,
    borderColor: '#8b5cf6'
  }]
}
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
const showInfo = ref(false)
const sectionRef = ref(null)
defineExpose({ sectionRef })
</script>

<style scoped>
section {
  scroll-margin-top: 80px;
}
</style>
