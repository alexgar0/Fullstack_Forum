<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { create_reply, get_topic_by_id } from '../api/endpoints';
import type { ReplyCreateDTO, ReplyDTO, TopicDTO } from '../api/dto';
import BaseButton from '../../../components/ui/BaseButton.vue';
import BaseTextArea from '../../../components/ui/BaseTextArea.vue';

const route = useRoute();
const router = useRouter();
const topic_id = computed(() => Number(route.params.id));
const topic = ref<TopicDTO>();
const reply_content = ref<string>('');
const reply_success = ref<string>('');
const reply_error = ref<string>('');
const error = ref<boolean>(false);

const currentPage = ref(1);
const limit = 10;

const totalPages = computed(() => {
    if (!topic.value?.pagination) return 1;
    return Math.ceil(topic.value.pagination.total_items / topic.value.pagination.limit);
});

async function fetchTopic(page: number) {
    if (!topic_id.value) return;

    if (page < 1 || (topic.value && page > totalPages.value && totalPages.value > 0)) return;

    error.value = false;
    const offset = (page - 1) * limit;

    try {
        topic.value = await get_topic_by_id(topic_id.value, offset, limit);
        currentPage.value = page;
    } catch (e) {
        error.value = true;
    }
}

function change_page(page: number) {
    fetchTopic(page);
    document.querySelector('#replies-section')?.scrollIntoView({ behavior: 'smooth' });
}


const formattedDate = (dateStr: string | Date) => {
    return new Date(dateStr).toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

function back_to_branch() {
    router.push({
        name: 'branch_detail',
        params: { id: topic.value?.branch_id }
    });
}

async function send_reply() {
    try {
        if (!topic.value) return;
        reply_error.value = '';
        reply_success.value = '';

        const new_reply: ReplyCreateDTO = {
            content: reply_content.value,
            topic_id: topic.value?.id
        };
        let created_reply: ReplyDTO = await create_reply(new_reply);
        reply_success.value = `Reply created`
        setTimeout(() => {
            router.go(0);
        }, 1000);
    }
    catch (e: any) {
        console.log(e);
        const detail = e.response?.data?.message;
        if (detail) {
            reply_error.value = detail;
        } else {
            reply_error.value = "Unexpected error";
        }
    }
}

onMounted(() => {
    fetchTopic(1);
});
</script>

<template>
    <div class="p-8 flex flex-col gap-6 max-w-5xl mx-auto">
        <div class="flex items-center gap-4">
            <button @click="back_to_branch"
                class="text-text-secondary hover:text-accent cursor-pointer transition-colors text-sm">
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
                        <span class="text-[10px] font-bold uppercase tracking-widest text-text-secondary">Created
                            at</span>
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

            <section class="flex flex-col gap-4">
                <div class="flex items-center gap-2 border-b border-primary-alt pb-4">
                    <h2 class="text-xl font-thin text-text-main">Replies</h2>
                    <span class="text-xs text-text-secondary bg-primary-alt px-2 py-0.5 rounded-full">
                        {{ topic.pagination?.total_items || 0 }}
                    </span>
                </div>

                <div v-if="topic.replies && topic.replies.length > 0" class="flex flex-col gap-4">
                    <div v-for="reply in topic.replies" :key="reply.id"
                        class="bg-primary/50 p-5 border border-primary-alt/50 rounded-sm hover:border-primary-alt transition-colors">

                        <div class="flex justify-between items-center mb-3 text-sm border-b border-primary-alt/30 pb-2">
                            <span class="text-accent font-medium">{{ reply.creator_username }}</span>
                            <span class="font-mono text-xs text-text-secondary">
                                {{ formattedDate(reply.created_at) }}
                            </span>
                        </div>

                        <p class="whitespace-pre-wrap leading-relaxed text-text-main font-light">
                            {{ reply.content }}
                        </p>
                    </div>

                    <div class="flex justify-between items-center mt-4 pt-4 border-t border-primary-alt">
                        <span class="text-sm text-text-secondary">
                            Page {{ currentPage }} of {{ totalPages }}
                        </span>
                        <div class="flex gap-2">
                            <BaseButton @click="change_page(currentPage - 1)" :disabled="currentPage <= 1"
                                class="bg-transparent border-primary-alt hover:bg-primary-alt w-32 disabled:opacity-50 disabled:cursor-not-allowed">
                                &larr; Prev
                            </BaseButton>
                            <BaseButton @click="change_page(currentPage + 1)" :disabled="currentPage >= totalPages"
                                class="w-32 disabled:opacity-50 disabled:cursor-not-allowed">
                                Next &rarr;
                            </BaseButton>
                        </div>
                    </div>
                </div>

                <div v-else class="text-center py-8 border border-dashed border-primary-alt/50 rounded-sm">
                    <p class="text-text-secondary font-light">No replies yet. Be the first to comment!</p>
                </div>
            </section>

            <footer class="flex flex-col gap-4 border-t border-primary-alt pt-6">
                <div class="w-full">
                    <p class="font-bold text-sm mb-1">Leave your reply</p>
                    <BaseTextArea class="bg-primary-alt w-full" v-model="reply_content"></BaseTextArea>
                </div>
                <div class="flex gap-2 self-end">
                    <BaseButton class="bg-transparent border-primary-alt hover:bg-primary-alt w-32">
                        Report
                    </BaseButton>
                    <BaseButton @click="send_reply" class="w-40">
                        Reply
                    </BaseButton>
                </div>
                <p v-if="reply_error" class="text-text-error">{{ reply_error }}</p>
                <p v-if="reply_success" class="text-accent">{{ reply_success }}</p>
            </footer>
        </div>
    </div>
</template>