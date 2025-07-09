<template>
  <div id="home" class="font-sans text-gray-900">
    <Hero @scrollToPredict="scrollToPredict" @scrollToHow="scrollToHow" />

    <section ref="howSection" class="py-20 bg-white text-center">
      <h2 class="text-3xl font-bold mb-6">How It Works</h2>
      <p class="max-w-2xl mx-auto text-lg">Animated walkthrough placeholder showing live API data, LSTM model and interactive chart.</p>
    </section>

    <section ref="predictSection" class="py-20 bg-gray-50">
      <div class="container mx-auto px-4 space-y-6">
        <div class="flex flex-col md:flex-row md:space-x-6">
          <div class="flex-1 space-y-6">
            <div class="card">
              <PredictButton />
            </div>
            <div class="card">
              <PredictionDetails ref="predictionDetailsRef" />
            </div>
            <div class="card">
              <PredictionInside :plotUrl="predictionPlotUrl" :featureImportanceUrl="featureImportanceUrl" :metrics="allMetrics" />
            </div>
            <div class="card">
              <PredictionTable />
            </div>
          </div>
          <div class="flex-1 space-y-6 mt-6 md:mt-0">
            <div class="card">
              <ConnectionStatus />
            </div>
            <div class="card">
              <StockChart />
            </div>
            <div class="card">
              <FetchButton :fetchCount="fetchCount" />
            </div>
            <div class="card">
              <DataChecker />
            </div>
          </div>
        </div>
      </div>
    </section>

    <Modal v-if="showModal" @close="closePredictionModal">
      <PredictionProgress :models="selectedModels" :abortSignal="predictionAbortController?.signal" @complete="handlePredictionComplete" />
    </Modal>

    <FetchLogsModal v-if="showFetchLogs" :logLines="fetchLogLines" @close="showFetchLogs = false" />
  </div>
</template>

<script setup>
import { ref, provide, watch, onMounted } from 'vue'
import { useScroll } from '@vueuse/core'

import Hero from '../components/Hero.vue'
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
const predictSection = ref(null)
const { y } = useScroll(window)

function scrollToHow() {
  howSection.value?.scrollIntoView({ behavior: 'smooth' })
}
function scrollToPredict() {
  predictSection.value?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.card {
  @apply bg-white rounded-xl shadow-md p-6;
}
</style>
