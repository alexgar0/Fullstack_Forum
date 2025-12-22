<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { logout, me } from './features/auth/api/endpoints';
import { user } from './features/auth/session';
import { onMounted } from 'vue';


onMounted(async () => {
  try {
    user.value = await me();
  } catch (e) {
    console.error(e);
  }
});

async function handle_logout() {
  await logout();
  user.value = undefined;
  window.location.href = '/login';
}

</script>

<template>
  <div class="min-h-screen">
    <header class="p-4 border-b border-slate-700 text-text-primary flex items-center gap-4">
      <RouterLink to="/" class="hover:underline">
        Home
      </RouterLink>
      <div class="flex gap-4 ml-auto">
        <p v-if="user">{{ user?.username }}</p>
        <RouterLink v-if="!user" to="/login" class="hover:underline">Login</RouterLink>
        <RouterLink v-if="!user" to="/register" class="hover:underline">Register</RouterLink>
        <button v-else @click="handle_logout" class="hover:underline">Logout</button>
      </div>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped></style>
