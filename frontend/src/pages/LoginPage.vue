<script setup lang="ts">
import { ref } from 'vue';
import { login } from '../api/users';

const username = ref('');
const password = ref('');
const error = ref('');

async function handleLogin() {
  try {
    await login(username.value, password.value);
    window.location.href = '/';
  }
  catch (e: any) {
    console.log(e);

    const detail = e.response?.data?.detail;

    if (detail) {
      error.value = detail;                 // показываем detail
    } else if (e.response?.status === 401) {
      error.value = "Invalid username or password";
    } else {
      error.value = "Unexpected error";
    }
  }
}

</script>


<template>
  <div class="flex flex-col items-center justify-center" style="height: calc(100vh - 64px);">
    <h1 class="text-3xl font-bold mb-4">Welcome</h1>

    <p v-if="error" class="text-text-error mb-4">{{ error }}</p>

    <div class="flex flex-col gap-4 w-64">
      <input type="text" placeholder="Username" v-model="username"
        class="p-2 rounded border border-primary-alt  bg-surface-alt" />

      <input type="password" placeholder="Password" v-model="password"
        class="p-2 rounded border border-primary-alt  bg-surface-alt" />
      <button @click="handleLogin"
        class="p-2 cursor-pointer rounded border border-primary-alt bg-primary text-text-primary">Login</button>
    </div>
  </div>
</template>
