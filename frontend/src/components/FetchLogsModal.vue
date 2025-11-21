<template>
  <div class="modal">
    <div class="modal-content">
      <button class="close-button" @click="emit('close')">×</button>
      <h3>Fetch Logs</h3>
      <div v-if="loading" class="progress-wrapper">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
        </div>
        <p class="helper">{{ statusMessage }}</p>
      </div>
      <pre class="log-output">
        <code>{{ logs.join('') }}</code>
      </pre>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const emit = defineEmits(['close'])

const logs = ref([])
const loading = ref(true)
const statusMessage = ref('Connecting to Alpha Vantage…')
const progress = ref(10)
let progressTimer = null

const stopProgress = () => {
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
}

const startProgress = () => {
  progress.value = 10
  stopProgress()
  progressTimer = setInterval(() => {
    if (progress.value < 80) {
      progress.value = Math.min(progress.value + 5, 80)
    }
  }, 300)
}

onMounted(async () => {
  startProgress()
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/fetch-latest-stream`, {
      method: 'POST'
    })

    const reader = res.body?.getReader()
    if (!reader) {
      throw new Error('No response body received')
    }

    const decoder = new TextDecoder('utf-8')

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value, { stream: true })
      if (chunk.trim()) {
        statusMessage.value = 'Processing latest response…'
        progress.value = Math.min(progress.value + 3, 90)
      }
      logs.value.push(chunk)
    }
    statusMessage.value = 'Finished fetching data.'
    progress.value = 100
  } catch (err) {
    logs.value.push('\nError during fetch:\n' + err.message)
    statusMessage.value = 'Fetch failed. Please try again.'
  }
  stopProgress()
  loading.value = false
})

onBeforeUnmount(() => {
  stopProgress()
})
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  position: relative;
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.log-output {
  background: #111;
  color: #0f0;
  padding: 1rem;
  border-radius: 8px;
  max-height: 60vh;
  overflow-y: auto;
  font-family: 'Fira Code', monospace;
  font-size: 0.85rem;
}

.close-button {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
}

.progress-wrapper {
  margin-bottom: 1rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #410093, #7e3ff2);
  transition: width 0.2s ease;
}

.helper {
  margin-top: 0.4rem;
  font-size: 0.85rem;
  color: #555;
}
</style>
