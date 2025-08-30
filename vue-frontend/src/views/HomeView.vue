<template>
  <div class="container">
    <h1>📄 Список страниц</h1>
    <ul>
      <li v-for="page in pages" :key="page.id">
        <router-link :to="`/pages/${page.id}`">{{ page.title }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const pages = ref([])

onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/pages/')
  const data = await res.json()
  pages.value = data.results
})
</script>