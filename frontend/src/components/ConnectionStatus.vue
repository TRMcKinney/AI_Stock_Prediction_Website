<template>
  <div class="connection-status">
    <h2>Connection Status (Backend)</h2>
    <p>
      <span :class="statusClass">●</span>
      {{ message }}
    </p>
    <button @click="checkBackend" :disabled="loading">
      {{ loading ? "Waking up..." : "Wake Backend" }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const message = ref("Checking backend...")
const statusClass = ref("status-loading")
const loading = ref(false)

const checkBackend = async () => {
  loading.value = true
  message.value = "Checking backend..."
  statusClass.value = "status-loading"

  try {
    await axios.get(`${import.meta.env.VITE_API_BASE_URL}/ping`)
    message.value = "Backend connected"
    statusClass.value = "status-ok"
  } catch (err) {
    console.error("Ping failed:", err)
    message.value = "Backend not reachable"
    statusClass.value = "status-error"
  }

  loading.value = false
}

// Run once on mount
checkBackend()
</script>


<style scoped>
.status-ok {
  color: green;
}
.status-loading {
  color: orange;
}
.status-error {
  color: red;
}

button {
  margin-top: 0.5rem;
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
  background-color: #0077cc;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:disabled {
  background-color: #999;
  cursor: wait;
}
</style>

