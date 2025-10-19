<template>
  <section class="hero">
    <h2>NBA 데이터 인사이트에 오신 것을 환영합니다.</h2>
    <p>최신 경기 데이터를 열람하고, 구독을 업그레이드하여 더 많은 통계를 확인하세요.</p>
    <RouterLink class="hero__cta" to="/data">데이터 둘러보기</RouterLink>
  </section>
</template>

<script setup>
</script>

<style scoped>
.hero {
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.1);
  text-align: center;
}

.hero__cta {
  display: inline-block;
  margin-top: 2rem;
  padding: 0.75rem 1.5rem;
  background: #2563eb;
  color: white;
  border-radius: 999px;
}
</style>
