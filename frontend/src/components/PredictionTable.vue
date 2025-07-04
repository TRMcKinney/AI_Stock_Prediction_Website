<template>
  <div>
    <h2>Prediction History</h2>
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Model</th>
          <th>% Change</th>
          <th>Predicted Price</th>
          <th>Actual Price</th>
          <th>Difference</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in history" :key="row.id">
          <td>{{ row.date_of_prediction }}</td>
          <td>{{ row.model_type }}</td>
          <td>{{ row.prediction?.toFixed(2) }}</td>
          <td>{{ row.predicted_price?.toFixed(2) }}</td>
          <td>{{ row.actual_price != null ? row.actual_price.toFixed(2) : '-' }}</td>
          <td>
            {{ row.difference != null ? row.difference.toFixed(2) : '-' }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

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
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  padding: 0.5rem;
  border: 1px solid #ccc;
  text-align: center;
}
</style>