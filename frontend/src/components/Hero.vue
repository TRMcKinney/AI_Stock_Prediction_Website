<template>
  <section class="relative flex flex-col items-center justify-center text-center h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white">
    <div v-motion="{ initial: { opacity: 0, y: 20 }, enter: { opacity: 1, y: 0, transition: { duration: 0.6 } } }">
      <h1 class="text-4xl md:text-6xl font-bold mb-4">AI-Powered Apple Stock Predictions</h1>
      <p class="text-lg md:text-2xl mb-8">Pulling real data. Predicting near-future trends.</p>
      <div class="flex space-x-4 justify-center">
        <button @click="$emit('scrollToPredict')" class="px-6 py-3 rounded-lg bg-purple-600 hover:bg-purple-700">View Latest Prediction</button>
        <button @click="$emit('scrollToHow')" class="px-6 py-3 rounded-lg bg-gray-800 hover:bg-gray-700">How It Works</button>
      </div>
    </div>
  </section>
</template>

<script setup>
// Emit events to scroll to sections
</script>

<style scoped>
</style>
