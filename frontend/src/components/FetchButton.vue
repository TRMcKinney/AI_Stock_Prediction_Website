<template>
  <div>
    <p class="description">
      Manual button to retrieve the latest stock data to circumnavigate payment required for setting up daily job which would automate this.
    </p>
    <p class="last-fetch" v-if="lastFetchDate">
      📅 Data Last Fetched: {{ lastFetchDate }}
    </p>
    <button @click="fetchData" :disabled="loading">
      {{ loading ? 'Fetching...' : 'Fetch Latest Stock Data' }}
    </button>
    <p v-if="message" class="status">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import axios from 'axios'

const loading = ref(false)
const message = ref('')
const lastFetchDate = ref(null)
const emit = defineEmits(['fetch-complete'])

const fetchLastDate = async () => {
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/last-fetch-date`)
    lastFetchDate.value = res.data.last_fetch
  } catch (err) {
    console.error("Failed to load last fetch date", err)
  }
}

const fetchData = async () => {
  loading.value = true
  message.value = ''

  try {
    const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/fetch-latest`)
    if (res.data.status === "success") {
      const count = res.data.uploaded ?? 0
      message.value =
        count > 0
          ? `Data fetch successful! ${count} records uploaded.`
          : `No new records — data is already up to date.`
      fetchLastDate() // updates the "Data Last Fetched" display
      emit('fetch-complete') // updates DataChecker.vue via App.vue
    } else {
      message.value = "Error: " + (res.data.output || res.data.message)
    }
  } catch (err) {
    console.error(err)
    message.value = "Server error."
  }

  loading.value = false
}

// load last fetch date on mount
onMounted(() => {
  fetchLastDate()
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
</style>
