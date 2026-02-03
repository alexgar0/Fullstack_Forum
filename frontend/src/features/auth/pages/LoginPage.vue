<script setup lang="ts">
import { ref } from 'vue';
import { login } from '../api/endpoints';
import { REGISTER_PATH } from '../router';
import BaseButton from '../../../components/ui/BaseButton.vue';
import BaseInput from '../../../components/ui/BaseInput.vue';

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

function handleSubmit(e?: Event) {
  e?.preventDefault(); // Предотвращаем перезагрузку страницы
  handleLogin();
}

</script>


<template>
  <div class="flex flex-col items-center justify-center" style="height: calc(100vh - 64px);">
    <h1 class="text-3xl font-bold mb-4">Welcome</h1>
    <p v-if="error" class="text-text-error mb-4">{{ error }}</p>
    <form @submit="handleSubmit" class="flex flex-col gap-4">
      <BaseInput v-model="username" placeholder="Username" type="text" class="w-full" />
      <BaseInput v-model="password" placeholder="Password" type="password" class="w-full" />
      <BaseButton type="submit" class="border-primary-alt bg-primary w-full">
        Login
      </BaseButton>
      <p class="text-sm text-text-secondary">If you don't have an account, you can <a class="text-accent"
          :href="REGISTER_PATH">register</a></p>
    </form>
  </div>
</template>
