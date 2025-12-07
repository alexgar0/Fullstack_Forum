<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen">
    <header class="p-4 border-b border-slate-700 flex gap-4">
      <RouterLink to="/" class="hover:underline">
        Home
      </RouterLink>
      <RouterLink to="/login" class="hover:underline">
        Login
      </RouterLink>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped></style>
