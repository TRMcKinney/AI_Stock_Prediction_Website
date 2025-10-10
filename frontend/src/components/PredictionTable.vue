<template>
  <div>
    <div class="flex items-center mb-2">
      <h2 class="text-lg font-semibold mr-4">Prediction History</h2>
      <button
        class="refresh-btn"
        :disabled="isRefreshing"
        @click="refreshHistory"
      >
        <span v-if="isRefreshing">Updating...</span>
        <span v-else>Update History</span>
      </button>
    </div>
    <p
      v-if="statusMessage"
      class="mb-3 text-sm"
      :class="statusType === 'error' ? 'text-red-600' : 'text-green-600'"
    >
      {{ statusMessage }}
    </p>
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

const history = ref([])
const isRefreshing = ref(false)
const statusMessage = ref('')
const statusType = ref('success')

async function loadHistory({ showErrors = false } = {}) {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/prediction-history`)
    if (!res.ok) {
      throw new Error(`Failed to load prediction history: ${res.status}`)
    }
    history.value = await res.json()
  } catch (err) {
    history.value = []
    console.error('Failed to load prediction history', err)
    if (showErrors) {
      statusMessage.value = 'Unable to load prediction history. Please try again later.'
      statusType.value = 'error'
    }
    throw err
  }
}

async function refreshHistory() {
  if (isRefreshing.value) return

  statusMessage.value = ''
  isRefreshing.value = true
  statusType.value = 'success'

  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/refresh-prediction-history`, {
      method: 'POST',
    })

    if (!res.ok) {
      throw new Error(`Failed to refresh prediction history: ${res.status}`)
    }

    let updatedCount = null
    try {
      const data = await res.json()
      updatedCount = typeof data?.updated === 'number' ? data.updated : null
    } catch (err) {
      updatedCount = null
    }

    await loadHistory()

    if (updatedCount === null) {
      statusMessage.value = 'Prediction history refreshed.'
    } else if (updatedCount === 0) {
      statusMessage.value = 'Prediction history is already up to date.'
    } else {
      statusMessage.value = `Updated ${updatedCount} record${updatedCount === 1 ? '' : 's'} with actual prices.`
    }
    statusType.value = 'success'
  } catch (err) {
    console.error('Failed to refresh prediction history', err)
    statusMessage.value = 'Failed to refresh prediction history. Please try again.'
    statusType.value = 'error'
  } finally {
    isRefreshing.value = false
  }
}

onMounted(() => {
  loadHistory({ showErrors: true }).catch(() => {})
})
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
.refresh-btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

