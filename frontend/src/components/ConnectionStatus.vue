<template>
  <div class="connection-status">
    <h2>Connection Status (Backend)</h2>
    <p>
      <span :class="statusClass">●</span>
      {{ message }}
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref("Checking backend...")
const statusClass = ref("status-loading")

onMounted(async () => {
  try {
    await axios.get(`${import.meta.env.VITE_API_BASE_URL}/ping`)
    message.value = "Backend connected"
    statusClass.value = "status-ok"
  } catch (err) {
    console.error("Ping failed:", err)
    message.value = "Backend not reachable"
    statusClass.value = "status-error"
  }
})
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
</style>
