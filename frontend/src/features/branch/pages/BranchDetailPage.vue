<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { get_branch } from '../api/endpoints';
import type { BranchWithSmallTopicsDTO } from '../api/dto';
import BaseButton from '../../../components/ui/BaseButton.vue';
import SmallTopicRow from '../../topic/ui/SmallTopicRow.vue';

const route = useRoute()
const branch_id = computed(() => Number(route.params.id))
const branch = ref<BranchWithSmallTopicsDTO>();

const show_error = ref<boolean>(false);
onMounted(async () => {
    if (!branch_id.value) {
        show_error.value = true;
        return
    }
    try {
        branch.value = await get_branch(branch_id.value);
    }
    catch (e: any) {
        show_error.value = true;
    }
});

</script>
<template>
    <div class="p-4 flex flex-col">
        <p v-if="show_error" class="text-3xl">Branch not found</p>
        <div v-if="branch" class="p-4">
            <div class="flex flex-row mb-4">
                <p class="text-3xl">{{ branch.title }}</p>
                <router-link :to="{ name: 'topic_create', params: { id: branch_id } }" custom v-slot="{ navigate }">
                    <BaseButton class="border-primary bg-primary ml-auto" @click="navigate">
                        Create topic
                    </BaseButton>
                </router-link>
            </div>
            <div class="flex flex-col">
                <div v-if="branch.small_topics && branch.small_topics.length > 0" class="flex flex-col mb-4">
                    <SmallTopicRow v-for="topic in branch.small_topics" :key="topic.id" :topic="topic"/>
                </div>

                <div v-else class="border border-dashed border-primary-alt p-12 flex justify-center items-center">
                    <p class="text-text-secondary font-thin italic">
                        There are no topics here yet. Be the first to start a discussion!
                    </p>
                </div>
            </div>
        </div>
    </div>

</template>