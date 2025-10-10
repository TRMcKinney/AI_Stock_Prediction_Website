<template>
  <div class="progress-container">
    <p>Running prediction...</p>
    <ul>
      <li v-for="m in models" :key="m.name">
        <span class="model-label">{{ m.label }}:</span>
        <span class="status" :class="m.status">
          <template v-if="m.status === 'running'">Running...</template>
          <template v-else-if="m.status === 'done'">
            Done<span v-if="m.duration"> ({{ m.duration.toFixed(1) }}s)</span>
          </template>
          <template v-else>Pending</template>
        </span>
      </li>
    </ul>
    <div class="overall-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: `${progressPercent}%` }"></div>
      </div>
      <p class="progress-text">Overall progress: {{ progressPercent }}%</p>
    </div>
    <div v-if="!allDone && !error" class="loader"></div>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const props = defineProps({
  models: {
    type: Array,
    default: () => ['baseline', 'cross_validation', 'persist', 'grid_search']
  },
  abortSignal: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['complete'])

const labelMap = {
  baseline: 'Baseline',
  cross_validation: 'Cross Validation',
  persist: 'Persisted',
  grid_search: 'Grid Search'
}
const models = ref(
  props.models.map((m) => ({
    name: m,
    label: labelMap[m] || m,
    status: 'pending',
    start: null,
    duration: null,
  }))
)

const results = ref(null)
const error = ref('')
const allDone = computed(() => models.value.every((m) => m.status === 'done'))
const completedCount = computed(() => models.value.filter((m) => m.status === 'done').length)
const progressPercent = computed(() => {
  if (models.value.length === 0) return 0
  return Math.round((completedCount.value / models.value.length) * 100)
})

function processLine(line) {
  if (line.startsWith('START:')) {
    const name = line.slice(6)
    const m = models.value.find((x) => x.name === name)
    if (m) {
      m.status = 'running'
      m.start = Date.now()
    }
  } else if (line.startsWith('END:')) {
    const name = line.slice(4)
    const m = models.value.find((x) => x.name === name)
    if (m) {
      m.status = 'done'
      if (m.start) m.duration = (Date.now() - m.start) / 1000
    }
  } else if (line.startsWith('RESULTS:')) {
    try {
      results.value = JSON.parse(line.slice(8))
    } catch (e) {
      error.value = 'Failed to parse results'
    }
  } else if (line.startsWith('ERROR:')) {
    error.value = line.slice(6)
  }
}

onMounted(async () => {
  try {
    const query = encodeURIComponent(props.models.join(','))
    const res = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/predict-stream?models=${query}`,
      { signal: props.abortSignal }
    )
    if (!res.ok) {
      error.value = `Server error: ${res.status}`
    } else {
      const reader = res.body.getReader()
      const decoder = new TextDecoder('utf-8')
      let buffer = ''
      while (true) {
        const { value, done } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()
        lines.forEach(processLine)
      }
      if (buffer) processLine(buffer)
    }
  } catch (err) {
    if (err.name !== 'AbortError') {
      error.value = err.message
    }
  }
  emit('complete', { results: results.value, error: error.value })
})
</script>

<style scoped>
.progress-container {
  text-align: left;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin: 0.25rem 0;
}
.model-label {
  font-weight: 600;
  margin-right: 0.25rem;
}
.status.done {
  color: green;
}
.status.running {
  color: #410093;
}
.status.pending {
  color: #666;
}
.loader {
  margin: 1rem auto;
  border: 6px solid #f3f3f3;
  border-top: 6px solid #410093;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.error {
  color: red;
  margin-top: 0.5rem;
}
.overall-progress {
  margin-top: 1rem;
}
.progress-bar {
  width: 100%;
  height: 10px;
  background: #e0e0e0;
  border-radius: 999px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #410093, #7e3ff2);
  transition: width 0.2s ease;
}
.progress-text {
  font-size: 0.9rem;
  color: #555;
  margin-top: 0.35rem;
}
</style>
