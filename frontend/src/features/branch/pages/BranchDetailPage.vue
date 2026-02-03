<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { get_branch } from '../api/endpoints';
import type { BranchDTO } from '../api/dto';
import { CREATE_TOPIC_PATH } from '../../topic/router';

const route = useRoute()
const branch_id = computed(() => Number(route.params.id))
const branch = ref<BranchDTO>();

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
        <div v-if="branch">
            <div class="flex flex-row">
                <p class="text-3xl">{{ branch.title }}</p>
                <button class="p-2 cursor-pointer rounded border border-primary-alt bg-primary ml-auto"><router-link
                        :to="{name:'create_topic', params: { id: branch_id }}">Create
                    topic</router-link></button>
            </div>
        </div>
    </div>

</template>