<script setup lang="ts">
import { ref } from 'vue';
import { register } from '../api/endpoints';
import { LOGIN_PATH, COMPLETE_REGISTRATION_PATH } from '../router';
const username = ref('');
const email = ref('');
const password = ref('');
const password_check = ref('');
const error = ref('');

async function handleRegister() {
    try {
        await register(username.value, email.value, password.value, password_check.value);
        window.location.href = COMPLETE_REGISTRATION_PATH;
    }
    catch (e: any) {
        console.log(e);

        const message = e.response?.data?.message;

        if (message) {
            error.value = message;                 // показываем detail
        } else if (e.response?.status === 401) {
            error.value = "Invalid username or password";
        } else {
            error.value = e;
        }
    }
}

</script>


<template>
    <div class="flex flex-col items-center justify-center" style="height: calc(100vh - 64px);">
        <h1 class="text-3xl font-bold mb-4">Registration</h1>

        <p v-if="error" class="text-text-error mb-4">{{ error }}</p>

        <div class="flex flex-col gap-4">
            <input type="text" placeholder="Username" v-model="username"
                class="p-2 rounded border border-primary-alt  bg-surface-alt" />

            <input type="text" placeholder="Email" v-model="email"
                class="p-2 rounded border border-primary-alt  bg-surface-alt" />

            <input type="password" placeholder="Password" v-model="password"
                class="p-2 rounded border border-primary-alt  bg-surface-alt" />
            <input type="password" placeholder="Retype password" v-model="password_check"
                class="p-2 rounded border border-primary-alt  bg-surface-alt" />
            <button @click="handleRegister"
                class="p-2 cursor-pointer rounded border border-primary-alt bg-primary">Login</button>
            <p class="text-sm text-text-secondary">If you already have an account, you can <a class="text-accent"
                    :href="LOGIN_PATH" >login</a></p>
        </div>
    </div>
</template>