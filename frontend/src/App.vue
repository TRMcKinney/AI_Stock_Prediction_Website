<template>
  <div id="app">
    <Header />

    <div class="page-intro">
      <PageIntro />
    </div>

    <main>
      <div class="content-row">
        
        <div class="left-column">
          <div class="card">
            <PredictButton />
          </div>
          <div class="card">
            <PredictionDetails ref="predictionDetailsRef" />
          </div>
          <div class="card">
            <PredictionInside
              :plotUrl="predictionPlotUrl"
              :featureImportanceUrl="featureImportanceUrl"
              :metrics="allMetrics"
            />
          </div>
          <div class="card">
            <PredictionTable />
          </div>
        </div>

        <div class="right-column">
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
    </main>

    <Modal v-if="showModal">
      <div>
        <p>{{ modalMessage }}</p>
        <div class="loader"></div>
      </div>
    </Modal>

    <FetchLogsModal
      v-if="showFetchLogs"
      :logLines="fetchLogLines"
      @close="showFetchLogs = false"
    />

    </div>
</template>






<script setup>
import { ref, provide, watch, onMounted } from 'vue'

import PredictButton from './components/PredictButton.vue'
import PredictionTable from './components/PredictionTable.vue'
import StockChart from './components/StockChart.vue'
import PageIntro from './components/PageIntro.vue'
import Header from './components/Header.vue'
import FetchButton from './components/FetchButton.vue'
import DataChecker from './components/DataChecker.vue'
import PredictionDetails from './components/PredictionDetails.vue'
import PredictionInside from './components/PredictionInside.vue'
import Modal from './components/Modal.vue'
import ConnectionStatus from './components/ConnectionStatus.vue'
import FetchLogsModal from './components/FetchLogsModal.vue'

// === PREDICTION MODAL ===
const showModal = ref(false)
const modalMessage = ref('Running prediction...')
const predictionDetailsRef = ref(null)
const predictionPlotUrl = ref('')
const featureImportanceUrl = ref('')
const allMetrics = ref({})

const triggerPrediction = async () => {
  showModal.value = true
  modalMessage.value = 'Running prediction...'
  const result = await predictionDetailsRef.value?.updatePrediction()
  predictionPlotUrl.value = result?.plotUrl || ''
  featureImportanceUrl.value = result?.featureImportanceUrl || ''
  allMetrics.value = result?.metrics || {}
  showModal.value = false
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

// === Row count trigger for DataChecker.vue ===
const rowCountTrigger = ref(0)
function handleFetchComplete() {
  rowCountTrigger.value++
  getFetchCount()
}

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
</script>









<style scoped>
#app {
  background-color: orange;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
  padding: 1rem;
}

/* Layout container for two columns */
.content-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: flex-start;
}

/* Left: button + table */
.left-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Right: chart + fetch button */
.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.page-intro {
  padding: 1rem;
}

.card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.loader {
  margin: 1.5rem auto 0;
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

</style>
