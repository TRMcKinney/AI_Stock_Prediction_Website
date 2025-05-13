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
            <PredictionTable />
          </div>
        </div>

        <div class="right-column">
          <div class="card">
            <StockChart />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import PredictButton from './components/PredictButton.vue'
import PredictionTable from './components/PredictionTable.vue'
import StockChart from './components/StockChart.vue'
import PageIntro from './components/PageIntro.vue'
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
}

/* Left: button + table */
.left-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Right: chart */
.right-column {
  flex: 1;
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
