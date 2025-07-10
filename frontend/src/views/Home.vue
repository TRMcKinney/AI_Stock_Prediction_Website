<template>
  <div id="home" class="font-sans text-gray-900">
    <NavBar :scrollToSection="scrollToSection" />
    <Hero @scrollToPredict="scrollToPredict" @scrollToHow="scrollToHow" />

    <section id="how" ref="howSection" class="py-20 bg-white text-center" v-motion="{ initial: { opacity: 0, y: 50 }, visibleOnce: { opacity: 1, y: 0 } }">
      <h2 class="text-3xl font-bold mb-10">How It Works</h2>
      <div class="max-w-5xl mx-auto grid md:grid-cols-3 gap-8">
        <div v-motion="{ initial: { opacity: 0, y: 30 }, visibleOnce: { opacity: 1, y: 0, transition: { delay: 0.1 } } }" class="p-6 rounded-lg shadow-md bg-gray-50">
          <div class="text-3xl mb-3">📡</div>
          <p>Our backend fetches the latest Apple stock prices directly from the market.</p>
        </div>
        <div v-motion="{ initial: { opacity: 0, y: 30 }, visibleOnce: { opacity: 1, y: 0, transition: { delay: 0.3 } } }" class="p-6 rounded-lg shadow-md bg-gray-50">
          <div class="text-3xl mb-3">🧠</div>
          <p>We use a trained deep learning model to predict near-future prices.</p>
        </div>
        <div v-motion="{ initial: { opacity: 0, y: 30 }, visibleOnce: { opacity: 1, y: 0, transition: { delay: 0.5 } } }" class="p-6 rounded-lg shadow-md bg-gray-50">
          <div class="text-3xl mb-3">📈</div>
          <p>You get an interactive chart with our prediction and trend insights.</p>
        </div>
      </div>
    </section>

    <section id="data" ref="dataSection" class="py-20 bg-gray-50" v-motion="{ initial: { opacity: 0, y: 50 }, visibleOnce: { opacity: 1, y: 0 } }">
      <div class="container mx-auto px-4 space-y-8">
        <div class="grid md:grid-cols-3 gap-6">
          <div class="space-y-6">
            <div class="card"><FetchButton :fetchCount="fetchCount" /></div>
            <div class="card"><DataChecker /></div>
            <div class="card"><ConnectionStatus /></div>
          </div>
          <div class="md:col-span-2">
            <div class="card h-full"><StockChart /></div>
          </div>
        </div>
      </div>
    </section>

    <section id="predict" ref="predictSection" class="py-20 bg-gray-100" v-motion="{ initial: { opacity: 0, y: 50 }, visibleOnce: { opacity: 1, y: 0 } }">
      <div class="container mx-auto px-4 space-y-6">
        <div class="card"><PredictButton /></div>
        <div class="card"><PredictionDetails ref="predictionDetailsRef" /></div>
        <div class="card"><PredictionInside :plotUrl="predictionPlotUrl" :featureImportanceUrl="featureImportanceUrl" :metrics="allMetrics" /></div>
      </div>
    </section>

    <section id="history" ref="historySection" class="py-20 bg-white" v-motion="{ initial: { opacity: 0, y: 50 }, visibleOnce: { opacity: 1, y: 0 } }">
      <div class="container mx-auto px-4 space-y-6">
        <div class="card"><PredictionTable /></div>
      </div>
    </section>

    <About />

    <Modal v-if="showModal" @close="closePredictionModal">
      <PredictionProgress :models="selectedModels" :abortSignal="predictionAbortController?.signal" @complete="handlePredictionComplete" />
    </Modal>

    <FetchLogsModal v-if="showFetchLogs" :logLines="fetchLogLines" @close="showFetchLogs = false" />
  </div>
</template>

<script setup>
import { ref, provide, watch, onMounted } from 'vue'

import Hero from '../components/Hero.vue'
import NavBar from '../components/NavBar.vue'
import About from '../components/About.vue'
import PredictButton from '../components/PredictButton.vue'
import PredictionTable from '../components/PredictionTable.vue'
import StockChart from '../components/StockChart.vue'
import FetchButton from '../components/FetchButton.vue'
import DataChecker from '../components/DataChecker.vue'
import PredictionDetails from '../components/PredictionDetails.vue'
import PredictionInside from '../components/PredictionInside.vue'
import PredictionProgress from '../components/PredictionProgress.vue'
import Modal from '../components/Modal.vue'
import ConnectionStatus from '../components/ConnectionStatus.vue'
import FetchLogsModal from '../components/FetchLogsModal.vue'

// === PREDICTION MODAL ===
const showModal = ref(false)
const predictionDetailsRef = ref(null)
const predictionPlotUrl = ref('')
const featureImportanceUrl = ref('')
const allMetrics = ref({})
const selectedModels = ref([])
let predictionAbortController = null

const triggerPrediction = (models) => {
  selectedModels.value = models
  predictionAbortController = new AbortController()
  showModal.value = true
}

function handlePredictionComplete({ results, error } = {}) {
  if (error) {
    console.error('Prediction error:', error)
    return
  }
  predictionDetailsRef.value?.setPredictionData(results || {})
  const baseline = results?.baseline || {}
  predictionPlotUrl.value = baseline.plot_base64 ? `data:image/png;base64,${baseline.plot_base64}` : ''
  featureImportanceUrl.value = baseline.importance_plot_base64 ? `data:image/png;base64,${baseline.importance_plot_base64}` : ''
  allMetrics.value = results || {}
  showModal.value = false
}

function closePredictionModal() {
  showModal.value = false
  if (predictionAbortController) {
    predictionAbortController.abort()
  }
}
provide('triggerPrediction', triggerPrediction)

watch(showModal, (isOpen) => {
  document.body.style.overflow = isOpen ? 'hidden' : 'auto'
})

// === FETCH LOGS MODAL ===
const showFetchLogs = ref(false)
const fetchCount = ref(null)

const triggerFetchLogs = () => {
  showFetchLogs.value = true
  getFetchCount()
}

provide('triggerFetchLogs', triggerFetchLogs)
provide('fetchCount', fetchCount)

// === Fetch API usage count from backend ===
const getFetchCount = async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/fetch-count`)
    const json = await res.json()
    fetchCount.value = json.count
  } catch (err) {
    fetchCount.value = null
  }
}

// Load fetch count on first mount
onMounted(() => {
  getFetchCount()
})

// === Smooth scroll helpers ===
const howSection = ref(null)
const dataSection = ref(null)
const predictSection = ref(null)
const historySection = ref(null)

function scrollToHow() {
  howSection.value?.scrollIntoView({ behavior: 'smooth' })
}
function scrollToPredict() {
  predictSection.value?.scrollIntoView({ behavior: 'smooth' })
}
function scrollToData() {
  dataSection.value?.scrollIntoView({ behavior: 'smooth' })
}

function scrollToSection(name) {
  if (name === 'home') {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }
  const map = { how: 'how', data: 'data', predict: 'predict', history: 'history', about: 'about' }
  const el = document.getElementById(map[name])
  el?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.card {
  @apply bg-white rounded-xl shadow-md p-6;
}
</style>
