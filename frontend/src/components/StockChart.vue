<template>
  <div class="w-full h-[400px]">
    <Line v-if="chartData" :data="chartData" :options="chartOptions" />
    <div v-else class="h-full flex items-center justify-center text-gray-400">
      No Data Available
    </div>
  </div>
</template>

<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, Filler)

defineProps({
  chartData: {
    type: Object,
    required: true
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      titleColor: '#1f2937',
      bodyColor: '#1f2937',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      padding: 10,
      displayColors: false
    }
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { maxTicksLimit: 10 }
    },
    y: {
      grid: { color: '#f3f4f6' },
      beginAtZero: false
    }
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false
  }
}
</script>
