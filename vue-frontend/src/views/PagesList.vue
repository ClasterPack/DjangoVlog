<template>
  <div class="container">
    <h1 class="title">📄 Список страниц</h1>
    <p class="meta">Всего: {{ count }} | Стр.: {{ page }} | Размер: {{ pageSize }}</p>

    <div v-if="loading" class="panel">Загрузка...</div>
    <div v-else-if="error" class="panel" style="color:#ff7a7a">Ошибка: {{ error }}</div>

    <div v-else class="panel">
      <div class="list">
        <div v-for="p in pages" :key="p.id" class="item">
          <div>
            <div style="font-weight:600">{{ p.title }}</div>
            <a :href="p.detail_url" target="_blank" rel="noopener" class="meta">JSON →</a>
          </div>
          <router-link :to="{ name:'page-detail', params: { id: p.id } }">
            <button>Показать контент</button>
          </router-link>
        </div>
      </div>

      <hr class="sep"/>

      <div class="actions">
        <button class="ghost" :disabled="!prev" @click="go(prev)">Назад</button>
        <button class="ghost" :disabled="!next" @click="go(next)">Вперед</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchJSON, pagesListUrl } from '../api'

const pages = ref([])
const next = ref(null)
const prev = ref(null)
const count = ref(0)
const page = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const error = ref('')

async function load(url = pagesListUrl(page.value, pageSize.value)) {
  loading.value = true
  error.value = ''
  try {
    const data = await fetchJSON(url)
    pages.value = data.results || []
    next.value = data.next
    prev.value = data.previous
    count.value = data.count || 0
    try {
      const u = new URL(url, window.location.origin)
      page.value = Number(u.searchParams.get('page') || 1)
      pageSize.value = Number(u.searchParams.get('page_size') || 10)
    } catch {}
  } catch (e) {
    error.value = String(e)
  } finally {
    loading.value = false
  }
}

function go(url) {
  if (url) load(url)
}

onMounted(() => load())
</script>