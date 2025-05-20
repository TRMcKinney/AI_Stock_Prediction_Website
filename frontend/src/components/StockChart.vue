<template>
  <div>
    <h2>
      Apple Stock Price History
      <span style="margin-left: 0.5rem; font-size: 0.9rem; color: #b35b00;">Last 100 days</span>
    </h2>
    <Line :data="chartData" :options="chartOptions" v-if="chartData" />
    <p v-else>Loading...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/stock-100`)
    const data = res.data
    console.log('API response:', data)

    chartData.value = {
      labels: data.map(d => {
        const date = new Date(d.date)
        return `${date.getDate().toString().padStart(2, '0')}/${
          (date.getMonth() + 1).toString().padStart(2, '0')
        }/${date.getFullYear()}`
      }),
      datasets: [
        {
          label: 'Close ($)',
          data: data.map(d => d.close),
          borderColor: '#410093',
          fill: false,
          tension: 0.2
        }
      ]
    }
  } catch (err) {
    console.error('Error loading chart data:', err)
  }
})
</script>


<style scoped>
canvas {
  width: 100% !important;
  max-width: 800px;
  height: 400px !important;
}
</style>