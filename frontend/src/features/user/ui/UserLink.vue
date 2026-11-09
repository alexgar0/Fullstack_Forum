<script setup lang="ts">
defineProps<{
  id: number
  username: string
}>()
</script>

<template>
  <router-link
    :to="{ name: 'user_profile', params: { id } }"
    class="hover:underline"
  >
    {{ username }}
  </router-link>
</template>
