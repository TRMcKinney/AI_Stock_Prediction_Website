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
            <PredictionTable />
          </div>
        </div>

        <div class="right-column">
          <div class="card">
            <StockChart />
          </div>
          <div class="card">
            <FetchButton />
          </div>
          <div class="card">
            <DataChecker />
          </div>
        </div>
      
      </div>
    </main>
  </div>
</template>



<script setup>

import { ref, provide } from 'vue'
import PredictButton from './components/PredictButton.vue'
import PredictionTable from './components/PredictionTable.vue'
import StockChart from './components/StockChart.vue'
import PageIntro from './components/PageIntro.vue'
import Header from './components/Header.vue'
import FetchButton from './components/FetchButton.vue'
import DataChecker from './components/DataChecker.vue'
import PredictionDetails from './components/PredictionDetails.vue'

const rowCountTrigger = ref(0)
function handleFetchComplete() {
  rowCountTrigger.value++  // triggers DataChecker to refetch from Supabase
}

const predictionDetailsRef = ref(null)
const triggerPrediction = () => {
  predictionDetailsRef.value?.updatePrediction()
}
provide('triggerPrediction', triggerPrediction)

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

</style>
