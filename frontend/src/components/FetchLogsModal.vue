<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
    <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
      
      <div class="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
        <h3 class="font-bold text-lg text-gray-800 flex items-center gap-2">
          <span v-if="loading" class="animate-spin text-purple-600">⟳</span>
          <span v-else class="text-green-600">✓</span>
          {{ statusMessage }}
        </h3>
        <button 
          @click="close" 
          :disabled="loading"
          class="text-gray-400 hover:text-gray-700 disabled:opacity-50 text-2xl leading-none"
        >
          &times;
        </button>
      </div>

      <div ref="logContainer" class="flex-1 bg-gray-900 p-4 overflow-y-auto font-mono text-sm">
        <div v-if="logs.length === 0" class="text-gray-500 italic">Initializing connection...</div>
        <div v-for="(line, i) in logs" :key="i" class="mb-1 break-words">
          <span class="text-green-400 font-bold mr-2">&gt;</span>
          <span class="text-gray-300">{{ line }}</span>
        </div>
      </div>

      <div class="p-4 border-t border-gray-100 bg-gray-50 text-right">
        <button 
          @click="close"
          class="px-5 py-2 rounded-lg font-medium transition-colors"
          :class="loading ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 'bg-purple-600 hover:bg-purple-700 text-white'"
          :disabled="loading"
        >
          {{ loading ? 'Running...' : 'Close & Refresh' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const emit = defineEmits(['close'])
const logs = ref([])
const loading = ref(true)
const statusMessage = ref('Connecting to backend...')
const logContainer = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
}

const close = () => {
  if (!loading.value) {
    emit('close')
  }
}

onMounted(async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/fetch-latest-stream`, {
      method: 'POST'
    })

    const reader = res.body?.getReader()
    if (!reader) throw new Error('No response body received')

    const decoder = new TextDecoder('utf-8')

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      // Split by newlines but keep lines that might be partial? 
      // Simplified for display:
      const lines = chunk.split('\n').filter(l => l.trim())
      
      logs.value.push(...lines)
      statusMessage.value = 'Fetching data...'
      scrollToBottom()
    }
    
    statusMessage.value = 'Sync Complete'
  } catch (err) {
    logs.value.push('Error: ' + err.message)
    statusMessage.value = 'Sync Failed'
  } finally {
    loading.value = false
    scrollToBottom()
  }
})
</script>