<template>
  <div id="app">
    <Header />
    <main>
      <PredictButton />
      <PredictionTable />
      <StockChart />
    </main>
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import PredictButton from './components/PredictButton.vue'
import PredictionTable from './components/PredictionTable.vue'
import StockChart from './components/StockChart.vue'
</script>

<style>
main {
  padding: 1rem;
  max-width: 800px;
  margin: auto;
}
</style>