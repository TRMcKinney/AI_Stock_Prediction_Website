<template>
  <div>
    <h2>Prediction Inside</h2>
    <img v-if="plotUrl" :src="plotUrl" alt="Prediction plot" />
    <div v-else class="placeholder"></div>
  </div>
</template>

<script setup>
const props = defineProps({
  plotUrl: {
    type: String,
    default: ''
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
</style>
