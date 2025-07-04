<template>
  <div>
    <button class="data-checker-btn" @click="fetchStats">Data Checker</button>
    <p>Total rows of data: <strong>{{ rowCount ?? '-' }}</strong></p>
    <p>Data Date Range: <strong>{{ dateRange ?? '-' }}</strong></p>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'

const rowCount = ref(null)
const dateRange = ref(null)

const fetchStats = async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/stock-stats`)
    const { count, min_date, max_date } = res.data

    rowCount.value = count ?? 'N/A'

    const format = (d) => new Date(d).toLocaleDateString("en-GB")
    dateRange.value = `${format(min_date)} – ${format(max_date)}`

  } catch (err) {
    console.error('Error fetching stock stats:', err)
    rowCount.value = 'Error'
    dateRange.value = 'Error'
  }
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
.data-checker-btn:hover {
  background-color: #5e2db7;
}
p {
  font-size: 1rem;
}
</style>
