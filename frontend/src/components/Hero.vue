<template>
  <section class="relative flex flex-col items-center justify-center text-center h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white">
    <div class="absolute inset-0 pointer-events-none opacity-20 flex items-center justify-center">
      <div class="text-7xl animate-bounce animated-apple">🍎</div>
    </div>
    <div v-motion="{ initial: { opacity: 0, y: 20 }, enter: { opacity: 1, y: 0, transition: { duration: 0.6 } } }" class="relative z-10">
      <h1 class="typewriter text-4xl md:text-6xl font-bold mb-4">AI-Powered Apple Stock Price Predictions</h1>
      <p class="text-lg md:text-2xl mb-8 fade-in">See what our deep learning model predicts for Apple's next move — based on real market data pulled live.</p>
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
.typewriter {
  overflow: hidden;
  border-right: 0.15em solid #fff;
  white-space: nowrap;
  animation: typing 3s steps(40, end), blink 0.75s step-end infinite;
}

.fade-in {
  animation: fadeIn 2s ease forwards;
}

.animated-apple {
  animation: float 4s ease-in-out infinite;
}

@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}

@keyframes blink {
  50% { border-color: transparent }
}

@keyframes fadeIn {
  from { opacity: 0 }
  to { opacity: 1 }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
