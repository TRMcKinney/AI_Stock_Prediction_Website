<template>
  <nav class="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-4 py-2 bg-white shadow dark:bg-gray-900 dark:text-white">
    <div class="flex space-x-4">
      <a href="#home" @click.prevent="scrollTo('home')" class="hover:underline">Home</a>
      <a href="#how" @click.prevent="scrollTo('how')" class="hover:underline">How It Works</a>
      <a href="#predict" @click.prevent="scrollTo('predict')" class="hover:underline">Prediction</a>
      <a href="#why-trust" @click.prevent="scrollTo('trust')" class="hover:underline">Why Trust It?</a>
      <a href="#about" @click.prevent="scrollTo('about')" class="hover:underline">About</a>
    </div>
    <button @click="isDark = !isDark" class="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700">
      <span v-if="isDark">🌙</span>
      <span v-else>☀️</span>
    </button>
  </nav>
</template>

<script setup>
import { ref, watch } from 'vue'
const props = defineProps(['scrollToSection'])
const isDark = ref(localStorage.getItem('theme') === 'dark')
watch(isDark, val => {
  const root = document.documentElement
  if (val) {
    root.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    root.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
})
function scrollTo(name) {
  props.scrollToSection?.(name)
}
</script>

<style scoped>
nav a {
  @apply px-2;
}
</style>
