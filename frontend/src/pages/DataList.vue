<template>
  <section>
    <header class="section-header">
      <h2>데이터셋</h2>
      <p>남은 조회 횟수: <strong>{{ remainingViews }}</strong></p>
    </header>
    <RouterLink v-if="remainingViews <= 0" class="upgrade" to="/upgrade">
      조회 한도를 초과했습니다. 업그레이드하기
    </RouterLink>
    <ul class="dataset-list">
      <li v-for="dataset in datasets" :key="dataset.id">
        <RouterLink :to="{ name: 'data-view', params: { id: dataset.id } }">
          {{ dataset.title }}
        </RouterLink>
        <span>{{ dataset.created_at }}</span>
      </li>
    </ul>
    <div v-if="!datasets.length" class="empty">아직 업로드된 데이터가 없습니다.</div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const datasets = ref([])
const remainingViews = ref(0)

onMounted(() => {
  // Placeholder fetch logic
  datasets.value = [
    { id: 1, title: '경기 요약 2024-01-01', created_at: '2024-01-02' }
  ]
  remainingViews.value = 3
})
</script>

<style scoped>
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1.5rem;
}

.upgrade {
  display: inline-block;
  margin-bottom: 1rem;
  color: #b91c1c;
}

.dataset-list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 1rem;
}

.dataset-list li {
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  display: flex;
  justify-content: space-between;
}

.empty {
  text-align: center;
  margin-top: 2rem;
  color: #6b7280;
}
</style>
