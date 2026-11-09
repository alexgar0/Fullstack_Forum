<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { SmallTopicDTO } from '../api/dto'
import { computed } from 'vue'
import UserLink from '../../user/ui/UserLink.vue'

const props = defineProps<{
  topic: SmallTopicDTO
}>()

const formattedDate = computed(() => {
  return new Date(props.topic.created_at).toLocaleString()
})

const router = useRouter()

function go_to_topic() {
  router.push({
    name: 'topic_view',
    params: { id: props.topic.id },
  })
}
</script>

<template>
  <div
    class="border border-primary-alt p-4 mb-2 flex flex-row items-center justify-between hover:bg-primary-alt transition-colors cursor-pointer"
    @click="go_to_topic"
  >
    <div class="flex items-center gap-4">
      <span class="text-text-secondary text-xs font-mono">#{{ topic.id }}</span>

      <h3 class="text-lg font-thin truncate max-w-md">
        {{ topic.title }}
      </h3>
    </div>

    <div class="flex items-center gap-6 text-sm text-text-secondary">
      <div class="flex flex-col items-end">
        <UserLink
          :id="topic.creator_id"
          :username="topic.creator_username"
          @click.stop
        />
      </div>

      <div class="flex flex-col items-end border-l border-primary-alt pl-6">
        <span>{{ formattedDate }}</span>
      </div>
    </div>
  </div>
</template>
