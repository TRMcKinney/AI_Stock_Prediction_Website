<template>
  <div>
    <div class="flex items-center mb-2">
      <h2 class="text-lg font-semibold mr-4">Prediction History</h2>
      <button class="refresh-btn" @click="refreshHistory">Update History</button>
    </div>
    <div class="overflow-x-auto">
      <table class="min-w-full text-sm text-center border">
        <thead class="bg-gray-100">
          <tr>
            <th class="py-2 px-3 border">Date</th>
            <th class="py-2 px-3 border">Model</th>
            <th class="py-2 px-3 border">% Change</th>
            <th class="py-2 px-3 border">Predicted Price</th>
            <th class="py-2 px-3 border">Actual Price</th>
            <th class="py-2 px-3 border">Difference</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in history" :key="row.id" class="even:bg-gray-50">
            <td class="py-2 px-3 border">{{ row.date_of_prediction }}</td>
            <td class="py-2 px-3 border">{{ row.model_type }}</td>
            <td class="py-2 px-3 border">{{ row.prediction?.toFixed(2) }}</td>
            <td class="py-2 px-3 border">{{ row.predicted_price?.toFixed(2) }}</td>
            <td class="py-2 px-3 border">{{ row.actual_price != null ? row.actual_price.toFixed(2) : '-' }}</td>
            <td class="py-2 px-3 border">
              {{ row.difference != null ? row.difference.toFixed(2) : '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

async function refreshHistory() {
  try {
    await fetch(`${import.meta.env.VITE_API_BASE_URL}/refresh-prediction-history`, { method: 'POST' })
    await loadHistory()
  } catch (err) {
    console.error('Failed to refresh prediction history', err)
  }
}

const history = ref([])

async function loadHistory() {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/prediction-history`)
    history.value = await res.json()
  } catch (err) {
    history.value = []
  }
}

onMounted(loadHistory)
</script>
<style scoped>
.refresh-btn {
  padding: 0.4rem 0.8rem;
  background-color: #2563eb;
  color: white;
  border-radius: 4px;
  font-size: 0.875rem;
}
.refresh-btn:hover {
  background-color: #1e4db7;
}
</style>