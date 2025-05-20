<template>
  <div>
    <h2>Data Checker</h2>
    <p>Total rows of data: <strong>{{ rowCount ?? 'Loading...' }}</strong></p>
    <p>Data Date Range: <strong>{{ dateRange ?? 'Loading...' }}</strong></p>
  </div>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  trigger: Number
})

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
    console.error("Error fetching stock stats:", err)
    rowCount.value = 'Error'
    dateRange.value = 'Error'
  }
}

// Fetch once on mount
onMounted(() => {
  fetchStats()
})

// Re-fetch on trigger change
watch(() => props.trigger, () => {
  fetchStats()
})
</script>

<style scoped>
h2 {
  margin-bottom: 0.5rem;
}
p {
  font-size: 1rem;
}
</style>
