<template>
    <div class="modal">
      <div class="modal-content">
        <button class="close-button" @click="emit('close')">×</button>
        <h3>Fetch Logs</h3>
        <pre class="log-output">
          <code>{{ logs.join('') }}</code>
        </pre>
      </div>
    </div>
  </template>
  
<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['close'])
  
  const logs = ref([])
  
  onMounted(async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/fetch-latest-stream`, {
        method: 'POST'
      })
  
      const reader = res.body.getReader()
      const decoder = new TextDecoder("utf-8")
  
      while (true) {
        const { value, done } = await reader.read()
        if (done) break
        const chunk = decoder.decode(value, { stream: true })
        logs.value.push(chunk)
      }
    } catch (err) {
      logs.value.push("\nError during fetch:\n" + err.message)
    }
  
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
  </style>
  