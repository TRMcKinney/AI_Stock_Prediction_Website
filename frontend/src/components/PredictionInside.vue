<template>
  <div class="space-y-6">
    <h2 class="text-xl font-semibold">Prediction Details</h2>
    <div v-if="plotUrl || featureImportanceUrl" class="grid md:grid-cols-2 gap-4">
      <div v-if="plotUrl" class="bg-gray-50 p-4 rounded-lg shadow">
        <h3 class="font-medium mb-2">Prediction vs Actual</h3>
        <img :src="plotUrl" alt="Prediction plot" class="w-full" />
      </div>
      <div v-if="featureImportanceUrl" class="bg-gray-50 p-4 rounded-lg shadow">
        <h3 class="font-medium mb-2">Feature Importance</h3>
        <img :src="featureImportanceUrl" alt="Feature importance plot" class="w-full" />
      </div>
    </div>
    <table
      v-if="Object.keys(metrics).length"
      class="w-full text-sm text-center border-collapse mt-4"
    >
      <thead class="bg-gray-100">
        <tr>
          <th class="py-2 px-3 border">Model</th>
          <th class="py-2 px-3 border">R2</th>
          <th class="py-2 px-3 border">MAE</th>
          <th class="py-2 px-3 border">RMSE</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(m, name) in metrics" :key="name" class="even:bg-gray-50">
          <td class="py-2 px-3 border font-medium">{{ name }}</td>
          <td class="py-2 px-3 border">{{ m.r2.toFixed(3) }}</td>
          <td class="py-2 px-3 border">{{ m.mae.toFixed(3) }}</td>
          <td class="py-2 px-3 border">{{ m.rmse.toFixed(3) }}</td>
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
  @apply w-full h-64 bg-gray-100 border border-dashed border-gray-300;
}
</style>
