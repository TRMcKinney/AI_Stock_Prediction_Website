<template>
  <section ref="sectionRef" class="py-20 bg-gray-50 dark:bg-gray-800 text-center">
    <h2 class="text-3xl font-bold mb-6 text-gray-900 dark:text-gray-100">About the Project</h2>
    <img class="w-32 h-32 rounded-full mx-auto mb-4" :src="photoUrl" alt="Author photo" />
    <p class="mb-4 text-gray-700 dark:text-gray-300">Built by Thomas R McKinney</p>
    <div class="space-x-4">
      <a class="text-purple-600 hover:underline" href="https://github.com/TRMcKinney" target="_blank" rel="noopener">GitHub</a>
      <a class="text-purple-600 hover:underline" href="mailto:contact@example.com">Contact</a>
    </div>
    <p class="mt-4 text-xs text-gray-500 dark:text-gray-400">
      Predictions are for educational purposes only and not financial advice.
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
const photoUrl = 'https://via.placeholder.com/150'
const sectionRef = ref(null)
defineExpose({ sectionRef })
</script>

<style scoped>
section {
  scroll-margin-top: 80px;
}
</style>
