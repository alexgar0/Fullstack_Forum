<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue';
import type { UserDTO } from './features/auth/api/dto';
import { logout, me } from './features/auth/api/endpoints';
import { user } from './features/auth/session';

async function get_user() {
  const response = await me();
  user.value = response;
  console.log(response);
}

async function handle_logout() {
  await logout();
  user.value = undefined;
  window.location.href = '/login';
}

get_user();

</script>

<template>
  <div class="min-h-screen">
    <header class="p-4 border-b border-slate-700 text-text-primary flex items-center gap-4">
      <RouterLink to="/" class="hover:underline">
        Home
      </RouterLink>
      <div class="flex gap-4 ml-auto">
        <p v-if="user" >{{ user?.username }}</p>
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
