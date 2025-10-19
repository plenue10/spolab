<template>
  <section class="login">
    <form class="card" @submit.prevent="handleLogin">
      <h2>로그인</h2>
      <input v-model="form.email" type="email" placeholder="이메일" required />
      <input v-model="form.password" type="password" placeholder="비밀번호" required />
      <button type="submit">로그인</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </section>
</template>

<script setup>
import { reactive, ref } from 'vue'

const form = reactive({ email: '', password: '' })
const error = ref('')

const handleLogin = () => {
  if (!form.email || !form.password) {
    error.value = '모든 필드를 입력하세요.'
    return
  }
  error.value = ''
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  width: min(360px, 100%);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.error {
  color: #dc2626;
}
</style>
