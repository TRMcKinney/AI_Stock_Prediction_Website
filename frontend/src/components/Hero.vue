<template>
  <section ref="vantaRef" class="relative flex flex-col items-center justify-center text-center h-screen overflow-hidden bg-white text-gray-900">
    <div v-motion="{ initial: { opacity: 0, y: 20 }, enter: { opacity: 1, y: 0, transition: { duration: 0.6 } } }" class="relative z-10">
      <h1 class="typewriter text-4xl md:text-6xl font-bold mb-4">AI-Powered Apple Stock Price Predictions</h1>
      <p class="text-lg md:text-2xl mb-8 fade-in">See what our deep learning model predicts for Apple's next move — based on real market data pulled live.</p>
      <!-- Navigation buttons moved to the banner -->
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const vantaRef = ref(null)
let vantaEffect = null

onMounted(() => {
  if (window.VANTA?.NET) {
    vantaEffect = window.VANTA.NET({
      el: vantaRef.value,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      color: 0xbbbbbb,
      backgroundColor: 0xffffff,
      points: 12.0,
      maxDistance: 20.0,
      spacing: 15.0
    })
  }
})

onUnmounted(() => {
  if (vantaEffect) vantaEffect.destroy()
})

</script>

<style scoped>
.typewriter {
  overflow: hidden;
  border-right: 0.15em solid #333;
  white-space: nowrap;
  animation: typing 3s steps(40, end), blink 0.75s step-end infinite;
}

.fade-in {
  animation: fadeIn 2s ease forwards;
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

</style>
