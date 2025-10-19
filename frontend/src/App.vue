<template>
  <div class="app">
    <header class="app__header">
      <h1>SPO Lab NBA Insights</h1>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/data">Data</RouterLink>
        <RouterLink to="/admin">Admin</RouterLink>
      </nav>
    </header>
    <main class="app__main">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.app {
  font-family: 'Inter', sans-serif;
  color: #1f2933;
  min-height: 100vh;
  background: #f3f4f6;
}

.app__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: #111827;
  color: white;
}

nav {
  display: flex;
  gap: 1.5rem;
}

a {
  color: inherit;
  text-decoration: none;
}

a.router-link-exact-active {
  font-weight: bold;
}

.app__main {
  padding: 2rem;
}
</style>
