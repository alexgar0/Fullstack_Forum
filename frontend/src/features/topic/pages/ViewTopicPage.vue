<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { get_topic_by_id } from '../api/endpoints';
import type { TopicDTO } from '../api/dto';
import BaseButton from '../../../components/ui/BaseButton.vue';

const route = useRoute();
const router = useRouter();
const topic_id = computed(() => Number(route.params.id));
const topic = ref<TopicDTO>();
const error = ref<boolean>(false);

const formattedDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

onMounted(async () => {
    if (!topic_id.value) {
        error.value = true;
        return;
    }
    try {
        topic.value = await get_topic_by_id(topic_id.value);
    } catch (e) {
        error.value = true;
    }
});
</script>

<template>
    <div class="p-8 flex flex-col gap-6 max-w-5xl mx-auto">
        <div class="flex items-center gap-4">
            <button @click="router.back()" class="text-text-secondary hover:text-accent cursor-pointer transition-colors text-sm">
                &larr; Back to branch
            </button>
        </div>

        <div v-if="error" class="text-text-error text-2xl font-thin">
            Topic not found or access denied.
        </div>

        <div v-if="topic" class="flex flex-col gap-8">
            <header class="border-b border-primary-alt pb-6">
                <h1 class="text-4xl font-thin mb-4">{{ topic.title }}</h1>
                
                <div class="flex items-center gap-6 text-sm">
                    <div class="flex flex-col">
                        <span class="text-[10px] font-bold uppercase tracking-widest text-text-secondary">Author</span>
                        <span class="text-accent">{{ topic.creator_username }}</span>
                    </div>
                    <div class="h-8 border-l border-primary-alt"></div>
                    <div class="flex flex-col">
                        <span class="text-[10px] font-bold uppercase tracking-widest text-text-secondary">Created at</span>
                        <span class="font-mono text-text-secondary">{{ formattedDate(topic.created_at) }}</span>
                    </div>
                    <div v-if="topic.last_edited_at !== topic.created_at" class="flex flex-col">
                        <span class="text-[10px] font-bold uppercase tracking-widest text-text-secondary">Edited</span>
                        <span class="font-mono text-text-secondary">{{ formattedDate(topic.last_edited_at) }}</span>
                    </div>
                </div>
            </header>

            <article class="bg-primary-alt/20 p-6 border border-primary-alt rounded-sm min-h-[200px]">
                <p class="whitespace-pre-wrap leading-relaxed font-light text-lg">
                    {{ topic.description }}
                </p>
            </article>

            <footer class="flex justify-end gap-4 border-t border-primary-alt pt-6">
                <BaseButton class="bg-transparent border-primary-alt hover:bg-primary-alt w-32">
                    Report
                </BaseButton>
                <BaseButton class="w-40">
                    Reply
                </BaseButton>
            </footer>
        </div>
    </div>
</template>