<template>
  <section class="admin">
    <h2>관리자 대시보드</h2>
    <div class="admin__grid">
      <form class="card" @submit.prevent="handleUpload">
        <h3>데이터 업로드</h3>
        <input v-model="form.title" type="text" placeholder="제목" required />
        <textarea v-model="form.description" placeholder="설명"></textarea>
        <input type="file" @change="onFileChange" accept=".csv,.json" required />
        <textarea v-model="form.notes" placeholder="비고"></textarea>
        <button type="submit">업로드</button>
        <p v-if="message" class="message">{{ message }}</p>
      </form>
      <div class="card">
        <h3>업로드 이력</h3>
        <ul>
          <li v-for="history in uploadHistory" :key="history.id">
            <strong>{{ history.title }}</strong>
            <span>{{ history.uploader }}</span>
            <span>{{ history.uploaded_at }}</span>
          </li>
        </ul>
      </div>
      <div class="card">
        <h3>사용자 권한 관리</h3>
        <p>역할별 조회 한도를 조정하고 구독을 관리하세요.</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive, ref } from 'vue'

const form = reactive({ title: '', description: '', notes: '', file: null })
const message = ref('')
const uploadHistory = ref([
  { id: 1, title: '시즌별 득점', uploader: 'admin@spolab.com', uploaded_at: '2024-02-01' }
])

const onFileChange = (event) => {
  const files = event.target.files
  form.file = files?.[0] ?? null
}

const handleUpload = () => {
  if (!form.file) {
    message.value = '파일을 선택하세요.'
    return
  }
  message.value = '업로드 요청이 전송되었습니다.'
}
</script>

<style scoped>
.admin__grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.card {
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

button {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 0.75rem;
}

.message {
  color: #10b981;
}
</style>
