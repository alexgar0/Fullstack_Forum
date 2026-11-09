<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ApiError } from '../../../api/openapi'
import { get_user_by_id } from '../../auth/api/endpoints'
import type { UserDTO } from '../../auth/api/dto'

const route = useRoute()
const profile = ref<UserDTO>()
const loading = ref(false)
const error = ref('')
let request_id = 0

watch(
  () => route.params.id,
  async (id) => {
    const current_request = ++request_id
    profile.value = undefined
    error.value = ''
    loading.value = false
    if (typeof id !== 'string' || !/^[1-9]\d*$/.test(id) || !Number.isSafeInteger(Number(id))) {
      error.value = 'User not found.'
      return
    }

    loading.value = true
    try {
      const result = await get_user_by_id(Number(id))
      if (current_request === request_id) profile.value = result
    } catch (e) {
      if (current_request === request_id) {
        error.value =
          e instanceof ApiError && e.status === 404
            ? 'User not found.'
            : e instanceof ApiError && (e.status === 401 || e.status === 403)
              ? 'Please log in to view this profile.'
              : 'Unable to load user profile. Please try again later.'
      }
    } finally {
      if (current_request === request_id) loading.value = false
    }
  },
  { immediate: true },
)

function formattedDate(date: string) {
  return new Date(date).toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <div class="p-8 flex flex-col gap-6 max-w-5xl mx-auto">
    <p
      v-if="loading"
      class="text-text-secondary"
      role="status"
    >
      Loading profile...
    </p>
    <p
      v-else-if="error"
      class="text-text-error text-2xl font-thin"
      role="alert"
    >
      {{ error }}
    </p>
    <section
      v-else-if="profile"
      class="flex flex-col gap-6"
    >
      <header class="border-b border-primary-alt pb-6">
        <h1 class="text-4xl font-thin mb-2">{{ profile.username }}</h1>
        <p class="text-text-secondary text-sm">{{ profile.role }}</p>
      </header>
      <div class="bg-primary-alt/20 p-6 border border-primary-alt rounded-sm">
        <h2 class="text-xl font-thin mb-3">About</h2>
        <p class="whitespace-pre-wrap font-light">{{ profile.bio || 'No bio yet.' }}</p>
      </div>
      <dl class="flex flex-wrap gap-6 text-sm">
        <div>
          <dt class="text-text-secondary">Joined</dt>
          <dd class="font-mono">{{ formattedDate(profile.created_at) }}</dd>
        </div>
        <div>
          <dt class="text-text-secondary">Last activity</dt>
          <dd class="font-mono">{{ formattedDate(profile.last_activity) }}</dd>
        </div>
        <div>
          <dt class="text-text-secondary">Views</dt>
          <dd class="font-mono">{{ profile.view_count }}</dd>
        </div>
      </dl>
    </section>
  </div>
</template>
