<template>
  <div>
    <h2>
      Apple Stock Price History
      <span style="margin-left: 0.5rem; font-size: 0.9rem; color: #b35b00;">Last 100 days</span>
    </h2>

    <div v-if="loading" class="progress-wrapper">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
      </div>
      <p class="progress-text">Preparing chart data ({{ progress }}%)</p>
    </div>

    <Line v-if="!loading && chartData" :data="chartData" :options="chartOptions" />
    <p v-else-if="!loading && !chartData && !error">No data available.</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const chartData = ref(null)
const loading = ref(true)
const error = ref('')
const progress = ref(0)
let progressTimer = null

const stopProgress = () => {
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
}

const startProgress = () => {
  progress.value = 5
  stopProgress()
  progressTimer = setInterval(() => {
    if (progress.value < 90) {
      progress.value = Math.min(progress.value + 7, 90)
    }
  }, 250)
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: {
      display: true,
      text: 'AAPL Stock Closing Price',
    }
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Date',
      }
    },
    y: {
      title: {
        display: true,
        text: 'Close Price ($)',
      }
    }
  }
}

onMounted(async () => {
  startProgress()
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/stock-100`)
    const payload = Array.isArray(res.data) ? res.data : []

    const sanitized = payload
      .filter((d) => d && d.date && d.close !== null && d.close !== undefined)
      .map((d) => ({
        date: new Date(d.date),
        close: Number.parseFloat(d.close)
      }))
      .filter((d) => !Number.isNaN(d.close) && !Number.isNaN(d.date.valueOf()))

    if (!sanitized.length) {
      throw new Error('No valid chart data returned.')
    }

    const latestHundred = sanitized
      .sort((a, b) => a.date - b.date)
      .slice(-100)

    chartData.value = {
      labels: latestHundred.map((d) =>
        `${d.date.getDate().toString().padStart(2, '0')}/${
          (d.date.getMonth() + 1).toString().padStart(2, '0')
        }/${d.date.getFullYear()}`
      ),
      datasets: [
        {
          label: 'Close ($)',
          data: latestHundred.map((d) => d.close),
          borderColor: '#410093',
          fill: false,
          tension: 0.2
        }
      ]
    }
    progress.value = 100
  } catch (err) {
    console.error('Error loading chart data:', err)
    error.value = 'Failed to load chart data. Please try again.'
  }
  stopProgress()
  loading.value = false
})

onBeforeUnmount(() => {
  stopProgress()
})
</script>


<style scoped>
canvas {
  width: 100% !important;
  max-width: 800px;
  height: 400px !important;
}

.progress-wrapper {
  margin: 1rem 0;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: #e0e0e0;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #410093, #7e3ff2);
  transition: width 0.2s ease;
}

.progress-text {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #555;
}

.error {
  color: #b00020;
  margin-top: 0.5rem;
}
</style>
