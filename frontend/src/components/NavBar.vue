<template>
  <nav class="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-4 py-2 bg-white shadow text-gray-900">
    <div class="flex space-x-4">
      <a href="#home" @click.prevent="scrollTo('home')" class="hover:underline">Home</a>
      <a href="#how" @click.prevent="scrollTo('how')" class="hover:underline">How It Works</a>
      <a href="#data" @click.prevent="scrollTo('data')" class="hover:underline">Data</a>
      <a href="#predict" @click.prevent="scrollTo('predict')" class="hover:underline">Predict</a>
      <a href="#history" @click.prevent="scrollTo('history')" class="hover:underline">History</a>
      <a href="#about" @click.prevent="scrollTo('about')" class="hover:underline">About</a>
    </div>
  </nav>
</template>

<script setup>
const props = defineProps(['scrollToSection'])
function scrollTo(name) {
  props.scrollToSection?.(name)
}
</script>

<style scoped>
nav a {
  @apply px-2;
}
</style>
