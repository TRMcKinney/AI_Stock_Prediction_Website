<template>
  <div>
    <p class="description">
      Manual button to retrieve the latest stock data to circumnavigate payment required for setting up daily job which would automate this. API rate limit is 25 requests per day - current requests number indicated next to button below.
    </p>

    <p class="last-fetch" v-if="lastFetchDate">
      📅 Data Last Fetched: {{ lastFetchDate }}
    </p>

    <button @click="fetchData" :disabled="loading">
      {{ loading ? 'Fetching...' : 'Fetch Latest Stock Data' }}
    </button>

    <span v-if="fetchCount !== null" class="request-count">
      ({{ fetchCount }} / 25 today)
    </span>

    <FetchLogsModal
      v-if="showModal"
      @close="handleModalClose"
      :onRefreshCount="refreshFetchCount"
    />

    <p v-if="message" class="status">{{ message }}</p>
  </div>
</template>

<script setup>
import { inject, ref, onMounted } from 'vue'
import axios from 'axios'
import FetchLogsModal from './FetchLogsModal.vue'

const loading = ref(false)
const message = ref('')
const lastFetchDate = ref(null)
const fetchCount = ref(null)
const showModal = ref(false)

const emit = defineEmits(['fetch-complete'])

const fetchWithLogs = inject('triggerFetchLogs')  // Not used anymore (replaced by modal toggle)

const fetchLastDate = async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/last-fetch-date`)
    lastFetchDate.value = res.data.last_fetch
  } catch (err) {
    console.error("Failed to load last fetch date", err)
  }
}

const refreshFetchCount = async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/fetch-count`)
    fetchCount.value = res.data.count
  } catch (err) {
    console.error("Failed to refresh fetch count", err)
  }
}

const fetchData = async () => {
  showModal.value = true
  loading.value = true
  message.value = ''
}

const handleModalClose = async () => {
  showModal.value = false
  loading.value = false
  await refreshFetchCount()
  await fetchLastDate()
  emit('fetch-complete')  // Optional: notify DataChecker.vue or others to re-query
}

// Load initial state on mount
onMounted(async () => {
  await fetchLastDate()
  await refreshFetchCount()
})
</script>

<style scoped>
.description {
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
  color: #333;
}

button {
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  background-color: #093;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #999;
  cursor: wait;
}

.status {
  margin-top: 0.5rem;
}

.request-count {
  margin-left: 0.5rem;
  font-size: 0.9rem;
  color: #555;
}

.last-fetch {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}
</style>
