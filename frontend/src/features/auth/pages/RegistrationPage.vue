<script setup lang="ts">
import { ref } from 'vue';
import { register } from '../api/endpoints';
import { LOGIN_PATH, COMPLETE_REGISTRATION_PATH } from '../router';
import BaseInput from '../../../components/ui/BaseInput.vue';
import BaseButton from '../../../components/ui/BaseButton.vue';

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
            error.value = message;
        } else if (e.response?.status === 401) {
            error.value = "Invalid username or password";
        } else {
            error.value = e;
        }
    }
}

function handleSubmit(e?: Event) {
    e?.preventDefault();
    handleRegister();
}

</script>
<template>
    <div class="flex flex-col items-center justify-center" style="height: calc(100vh - 64px);">
        <h1 class="text-3xl font-bold mb-4">Registration</h1>
        <p v-if="error" class="text-text-error mb-4">{{ error }}</p>
        <form @submit="handleSubmit" class="flex flex-col gap-4">
            <BaseInput v-model="username" placeholder="Username" type="text" />
            <BaseInput v-model="email" placeholder="Email" type="text" />
            <BaseInput v-model="password" placeholder="Password" type="password" />
            <BaseInput v-model="password_check" placeholder="Retype password" type="password" />
            <BaseButton type="submit" class="border-primary-alt bg-primary w-full">
                Register
            </BaseButton>
            <p class="text-sm text-text-secondary">If you already have an account, you can <a class="text-accent"
                    :href="LOGIN_PATH">login</a></p>
        </form>
    </div>
</template>