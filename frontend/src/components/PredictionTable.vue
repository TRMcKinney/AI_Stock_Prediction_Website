<template>
  <div>
    <h2>
      Prediction History
      <span style="margin-left: 0.5rem; font-size: 0.9rem; color: #b35b00;">Work In Progress</span>
    </h2>
    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Predicted Price</th>
          <th>Actual Price</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in fakeData" :key="entry.date">
          <td>{{ entry.date }}</td>
          <td>{{ entry.predicted }}</td>
          <td>{{ entry.actual }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const fakeData = [
  { date: '2025-04-01', predicted: 42.1, actual: 41.9 },
  { date: '2025-03-21', predicted: 40.2, actual: 40.7 },
  { date: '2025-03-11', predicted: 39.8, actual: 39.4 },
]
</script>

<style scoped>
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