<template>
  <div>
    <h2>Prediction Details</h2>
    <div v-if="plotUrl">
      <h3>Prediction vs Actual</h3>
      <img :src="plotUrl" alt="Prediction plot" />
    </div>
    <div v-if="featureImportanceUrl" class="metric">
      <h3>Feature Importance</h3>
      <img :src="featureImportanceUrl" alt="Feature importance plot" />
    </div>
    <p>R2 Score: {{ r2.toFixed(3) }}</p>
    <p>MAE: {{ mae.toFixed(3) }}</p>
    <p>RMSE: {{ rmse.toFixed(3) }}</p>
    <div v-if="!plotUrl" class="placeholder"></div>
  </div>
</template>

<script setup>
const props = defineProps({
  plotUrl: {
    type: String,
    default: ''
  },
  featureImportanceUrl: {
    type: String,
    default: ''
  },
  r2: {
    type: Number,
    default: 0
  },
  mae: {
    type: Number,
    default: 0
  },
  rmse: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
.placeholder {
  width: 100%;
  height: 300px;
  background-color: #f3f3f3;
  border: 1px dashed #ccc;
}
.metric {
  margin-top: 1rem;
}
</style>
