<template>
  <header class="header">
    <div class="header-inner">
      <button class="ghost" @click="goBack">← Назад</button>
      <h2 class="title" style="margin-left:.5rem">{{ pageData?.title || 'Страница' }}</h2>
      <span v-if="pageData" class="badge" style="margin-left:auto">ID: {{ pageData.id }}</span>
    </div>
  </header>

  <div class="container" style="margin-top:1rem">
    <div v-if="loading" class="panel">Загрузка...</div>
    <div v-else-if="error" class="panel" style="color:#ff7a7a">Ошибка: {{ error }}</div>

    <div v-else-if="pageData" class="panel">
      <h3 style="margin-top:0">Контент</h3>
      <div class="list">
        <div v-for="c in pageData.contents" :key="c.type + '-' + c.id" class="item" style="align-items:flex-start">
          <div>
            <div class="badge" style="margin-bottom:.25rem">Тип: {{ c.type }}</div>
            <div style="font-weight:600">{{ c.title }}</div>
            <div class="meta">Просмотры: {{ c.counter }}</div>

            <template v-if="c.type==='video'">
              <div class="meta">Видео: <a :href="c.video_url" target="_blank" rel="noopener">{{ c.video_url }}</a></div>
              <div class="meta" v-if="c.subtitles_url">Субтитры: <a :href="c.subtitles_url" target="_blank" rel="noopener">{{ c.subtitles_url }}</a></div>
            </template>

            <template v-else-if="c.type==='audio'">
              <div class="meta">Описание:</div>
              <pre style="white-space:pre-wrap; font-family:inherit; color:#ccd">{{ c.transcript }}</pre>
            </template>
          </div>
        </div>
      </div>
      <div class="actions" style="margin-top:1rem">
        <button class="ghost" @click="refresh">Обновить</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchJSON, pageDetailUrl } from '../api'

const route = useRoute()
const router = useRouter()

const pageId = ref(Number(route.params.id))
const pageData = ref(null)
const loading = ref(false)
const error = ref('')

async function load() {
  if (!pageId.value) return
  loading.value = true
  error.value = ''
  try {
    const data = await fetchJSON(pageDetailUrl(pageId.value))
    pageData.value = data
  } catch (e) {
    error.value = String(e)
  } finally {
    loading.value = false
  }
}

function goBack() {
  if (window.history.length > 1) router.back()
  else router.push({ name: 'pages' })
}

function refresh() {
  load()
}

watch(() => route.params.id, (val) => {
  pageId.value = Number(val)
  load()
})

onMounted(load)
</script>