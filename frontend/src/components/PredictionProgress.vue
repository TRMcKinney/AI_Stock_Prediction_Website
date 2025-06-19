<template>
  <div class="progress-container">
    <p>Running prediction...</p>
    <ul>
      <li v-for="m in models" :key="m.name">
        <label>
          <input type="checkbox" disabled :checked="m.done" />
          {{ m.label }}
        </label>
      </li>
    </ul>
    <div class="loader"></div>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['complete'])

const models = ref([
  { name: 'baseline', label: 'Baseline', done: false },
  { name: 'cross_validation', label: 'Cross Validation', done: false },
  { name: 'persist', label: 'Persisted', done: false },
  { name: 'grid_search', label: 'Grid Search', done: false }
])

const results = ref(null)
const error = ref('')

function processLine(line) {
  if (line.startsWith('END:')) {
    const name = line.slice(4)
    const m = models.value.find(x => x.name === name)
    if (m) m.done = true
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
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/predict-stream`)
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
  } catch (err) {
    error.value = err.message
  }
  emit('complete', results.value)
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
</style>
