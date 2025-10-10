<template>
  <div>
    <button class="data-checker-btn" @click="fetchStats" :disabled="loading">
      {{ loading ? 'Checking data…' : 'Data Checker' }}
    </button>
    <div v-if="loading" class="progress-wrapper">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
      </div>
      <p class="helper">Verifying dataset health…</p>
    </div>
    <p>Total rows of data: <strong>{{ rowCount ?? '-' }}</strong></p>
    <p>Data Date Range: <strong>{{ dateRange ?? '-' }}</strong></p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'

const rowCount = ref(null)
const dateRange = ref(null)
const loading = ref(false)
const progress = ref(0)
const error = ref('')
let progressTimer = null

const stopProgress = () => {
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
}

const startProgress = () => {
  progress.value = 10
  stopProgress()
  progressTimer = setInterval(() => {
    if (progress.value < 85) {
      progress.value = Math.min(progress.value + 8, 85)
    }
  }, 250)
}

const fetchStats = async () => {
  try {
    loading.value = true
    error.value = ''
    startProgress()
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/stock-stats`)
    const { count, min_date, max_date } = res.data

    rowCount.value = count ?? 'N/A'

    const format = (d) => (d ? new Date(d).toLocaleDateString('en-GB') : 'N/A')
    dateRange.value = `${format(min_date)} – ${format(max_date)}`
    progress.value = 100
  } catch (err) {
    console.error('Error fetching stock stats:', err)
    rowCount.value = 'Error'
    dateRange.value = 'Error'
    error.value = 'Unable to load stats right now.'
  }
  stopProgress()
  loading.value = false
}
</script>

<style scoped>
.data-checker-btn {
  display: block;
  padding: 0.6rem 1.2rem;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  background-color: #410093;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.data-checker-btn:disabled {
  background-color: #888;
  cursor: wait;
}
.data-checker-btn:hover {
  background-color: #5e2db7;
}
p {
  font-size: 1rem;
}
.progress-wrapper {
  margin: 0.75rem 0;
}
.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 999px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #410093, #7e3ff2);
  transition: width 0.2s ease;
}
.helper {
  font-size: 0.85rem;
  color: #555;
  margin-top: 0.4rem;
}
.error {
  margin-top: 0.5rem;
  color: #b00020;
}
</style>
