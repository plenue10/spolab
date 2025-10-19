<template>
  <section class="detail">
    <header>
      <h2>{{ dataset.title }}</h2>
      <p>{{ dataset.description }}</p>
    </header>
    <article class="detail__content">
      <pre>{{ dataset.preview }}</pre>
    </article>
    <footer class="detail__footer" v-if="overLimit">
      <p class="warning">조회 한도를 초과했습니다. <RouterLink to="/upgrade">업그레이드</RouterLink> 해 보세요.</p>
    </footer>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const dataset = ref({ title: '', description: '', preview: '' })
const overLimit = ref(false)
const route = useRoute()

onMounted(() => {
  const id = route.params.id
  dataset.value = {
    title: `데이터셋 #${id}`,
    description: '샘플 데이터 설명',
    preview: 'team,score\nSPO,102\nLAB,98'
  }
  overLimit.value = route.query.limit === 'exceeded'
})
</script>

<style scoped>
.detail {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
}

.detail__content {
  margin-top: 1.5rem;
  background: #111827;
  color: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.75rem;
  overflow-x: auto;
}

.warning {
  margin-top: 1.5rem;
  color: #b91c1c;
}
</style>
