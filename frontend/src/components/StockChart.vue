<template>
  <div>
    <h2>Yahoo Stock Price History</h2>
    <LineChart :chart-data="chartData" :chart-options="chartOptions" />
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

const LineChart = Line
const chartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Close Price ($)',
      data: [],
      fill: false,
      borderColor: '#410093',
      tension: 0.1
    }
  ]
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: false
    }
  }
}

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/stock-history')  // your FastAPI endpoint
  const prices = res.data

  chartData.value.labels = prices.map(d => d.Date)
  chartData.value.datasets[0].data = prices.map(d => d.Close)
})
</script>