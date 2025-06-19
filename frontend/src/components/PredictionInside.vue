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
    <table v-if="Object.keys(metrics).length">
      <thead>
        <tr>
          <th>Model</th>
          <th>R2</th>
          <th>MAE</th>
          <th>RMSE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(m, name) in metrics" :key="name">
          <td>{{ name }}</td>
          <td>{{ m.r2.toFixed(3) }}</td>
          <td>{{ m.mae.toFixed(3) }}</td>
          <td>{{ m.rmse.toFixed(3) }}</td>
        </tr>
      </tbody>
    </table>
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
  metrics: {
    type: Object,
    default: () => ({})
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
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  padding: 0.5rem;
  border: 1px solid #ccc;
  text-align: center;
}
</style>
