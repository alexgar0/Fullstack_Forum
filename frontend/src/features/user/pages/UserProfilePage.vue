<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ApiError } from '../../../api/openapi'
import { get_user_by_id } from '../../auth/api/endpoints'
import type { UserDTO } from '../../auth/api/dto'
import { get_user_topics } from '../api/endpoints'
import type { UserTopicsDTO } from '../api/dto'
import SmallTopicRow from '../../topic/ui/SmallTopicRow.vue'

const route = useRoute()
const profile = ref<UserDTO>()
const loading = ref(false)
const error = ref('')
const topics = ref<UserTopicsDTO>()
const topics_loading = ref(false)
const topics_error = ref('')
const topics_offset = ref(0)
let request_id = 0
let topics_request_id = 0

async function load_topics(user_id: number, offset = 0) {
  const current_request = ++topics_request_id
  topics_offset.value = offset
  topics_loading.value = true
  topics_error.value = ''
  try {
    const result = await get_user_topics(user_id, offset)
    if (current_request === topics_request_id) topics.value = result
  } catch {
    if (current_request === topics_request_id) {
      topics_error.value = 'Unable to load topics. Please try again later.'
    }
  } finally {
    if (current_request === topics_request_id) topics_loading.value = false
  }
}

watch(
  () => route.params.id,
  async (id) => {
    const current_request = ++request_id
    ++topics_request_id
    profile.value = undefined
    topics.value = undefined
    topics_loading.value = false
    topics_error.value = ''
    error.value = ''
    loading.value = false
    if (typeof id !== 'string' || !/^[1-9]\d*$/.test(id) || !Number.isSafeInteger(Number(id))) {
      error.value = 'User not found.'
      return
    }

    loading.value = true
    try {
      const result = await get_user_by_id(Number(id))
      if (current_request === request_id) {
        profile.value = result
        void load_topics(result.id)
      }
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
      <section>
        <h2 class="text-2xl font-thin mb-3">Topics</h2>
        <p
          v-if="topics_loading"
          class="text-text-secondary"
          role="status"
        >
          Loading topics...
        </p>
        <div
          v-else-if="topics_error"
          role="alert"
        >
          <p class="text-text-error">{{ topics_error }}</p>
          <button
            type="button"
            class="border border-primary-alt px-3 py-1 mt-2"
            @click="load_topics(profile.id, topics_offset)"
          >
            Retry
          </button>
        </div>
        <template v-else-if="topics">
          <p
            v-if="topics.items.length === 0"
            class="text-text-secondary"
          >
            No topics yet.
          </p>
          <SmallTopicRow
            v-for="topic in topics.items"
            :key="topic.id"
            :topic="topic"
          />
          <div
            v-if="topics.total_items > topics.limit"
            class="flex items-center gap-4 mt-4"
          >
            <button
              type="button"
              class="border border-primary-alt px-3 py-1 disabled:opacity-50"
              :disabled="topics.current_offset === 0"
              @click="load_topics(profile.id, Math.max(0, topics.current_offset - topics.limit))"
            >
              Previous
            </button>
            <span class="text-text-secondary"
              >{{ topics.current_offset + 1 }}–{{
                Math.min(topics.current_offset + topics.items.length, topics.total_items)
              }}
              / {{ topics.total_items }}</span
            >
            <button
              type="button"
              class="border border-primary-alt px-3 py-1 disabled:opacity-50"
              :disabled="topics.current_offset + topics.limit >= topics.total_items"
              @click="load_topics(profile.id, topics.current_offset + topics.limit)"
            >
              Next
            </button>
          </div>
        </template>
      </section>
    </section>
  </div>
</template>
