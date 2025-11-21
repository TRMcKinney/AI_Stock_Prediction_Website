<template>
  <div class="bg-white rounded-xl shadow-md overflow-hidden">
    <div class="p-6 border-b border-gray-100 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div>
        <h2 class="text-xl font-bold text-gray-900">Market Data</h2>
        <div class="flex items-center gap-3 text-sm mt-1">
           <span :class="connectionStatusClass" class="flex items-center gap-1 font-medium">
             ● {{ connectionMessage }}
           </span>
           <span class="text-gray-400">|</span>
           <span class="text-gray-600">
             Rows: <strong>{{ stats.count ?? '-' }}</strong>
           </span>
           <span class="text-gray-400">|</span>
           <span class="text-gray-600">
             Range: <strong>{{ formatDate(stats.min_date) }} - {{ formatDate(stats.max_date) }}</strong>
           </span>
        </div>
      </div>
      
      <button 
        @click="showSyncModal = true" 
        class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors flex items-center gap-2 shadow-sm"
      >
        <span>Sync Latest Data</span>
      </button>
    </div>

    <div class="p-6 relative min-h-[400px]">
      <div v-if="isLoadingInitial" class="absolute inset-0 flex items-center justify-center bg-white z-10">
        <p class="text-gray-500 animate-pulse">Loading chart data...</p>
      </div>
      
      <div v-if="error" class="p-4 bg-red-50 text-red-700 rounded-lg mb-4">
        {{ error }}
      </div>

      <StockChart v-if="chartData" :chart-data="chartData" />
    </div>

    <FetchLogsModal v-if="showSyncModal" @close="handleSyncComplete" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import StockChart from './StockChart.vue'
import FetchLogsModal from './FetchLogsModal.vue'

// State
const stats = ref({ count: null, min_date: null, max_date: null })
const chartData = ref(null)
const showSyncModal = ref(false)
const isLoadingInitial = ref(true)
const error = ref('')
const isBackendAlive = ref(false)

// Computed
const connectionMessage = computed(() => isBackendAlive.value ? 'Backend Connected' : 'Connecting...')
const connectionStatusClass = computed(() => isBackendAlive.value ? 'text-green-600' : 'text-orange-500')

// Helpers
const formatDate = (d) => d ? new Date(d).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: '2-digit' }) : '-'
const API_URL = import.meta.env.VITE_API_BASE_URL

// Lifecycle
onMounted(init)

async function init() {
  try {
    // 1. Check if backend is awake
    await fetch(`${API_URL}/ping`)
    isBackendAlive.value = true
    
    // 2. Load data
    await refreshAll()
  } catch (e) {
    console.error(e)
    error.value = "Could not connect to backend. Please ensure Render service is active."
  } finally {
    isLoadingInitial.value = false
  }
}

async function refreshAll() {
  await Promise.all([fetchStats(), fetchChart()])
}

async function fetchStats() {
  try {
    const res = await fetch(`${API_URL}/stock-stats`)
    if (res.ok) {
      stats.value = await res.json()
    }
  } catch (e) {
    console.error("Failed to load stats", e)
  }
}

async function fetchChart() {
  try {
    const res = await fetch(`${API_URL}/stock-100`)
    const raw = await res.json()
    
    if (!raw || !raw.length) return
    
    // Transform data for the simplified StockChart component
    const processed = raw.map(d => ({
      x: new Date(d.date).toLocaleDateString('en-GB'),
      y: d.close
    }))

    chartData.value = {
      labels: processed.map(p => p.x),
      datasets: [{
        label: 'AAPL Close ($)',
        data: processed.map(p => p.y),
        borderColor: '#7c3aed',
        backgroundColor: 'rgba(124, 58, 237, 0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 4
      }]
    }
  } catch (e) {
    console.error("Failed to load chart", e)
  }
}

async function handleSyncComplete() {
  showSyncModal.value = false
  // Re-fetch everything to show the new data on the chart
  await refreshAll()
}
</script>