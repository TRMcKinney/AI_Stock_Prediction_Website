<template>
  <div>
    <h2>Data Checker</h2>
    <p>Total rows of data: <strong>{{ totalRows }}</strong></p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const totalRows = ref('...')

onMounted(async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/row-count`)
    totalRows.value = res.data.count
  } catch (err) {
    console.error('❌ Error fetching row count:', err)
    totalRows.value = 'Error'
  }
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
