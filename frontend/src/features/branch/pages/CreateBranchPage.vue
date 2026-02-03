<script setup lang="ts">
import type { BranchCreateDTO, BranchDTO } from "../api/dto";
import { onMounted, ref } from "vue";
import { create_branch, get_all_branches } from "../api/endpoints";

import BaseButton from "../../../components/ui/BaseButton.vue";
import BaseInput from "../../../components/ui/BaseInput.vue";
import BaseTextArea from "../../../components/ui/BaseTextArea.vue";

const title = ref<string>('');
const description = ref<string>('');
const parent_id = ref<number | undefined>(undefined);

const error = ref<string>('');
const success = ref<string>('');

const all_branches = ref<BranchDTO[]>([]);
onMounted(async () => {
    try {
        all_branches.value = await get_all_branches();
    } catch (e) {
        error.value = 'Не удалось загрузить данные';
        console.error(e);
    }
});

async function handle_create() {
    try {
        error.value = '';
        success.value = '';
        const new_branch: BranchCreateDTO = {
            title: title.value,
            description: description.value,
        }
        let created_branch: BranchDTO = await create_branch(new_branch);
        success.value = `Branch ${created_branch.title} created`
    }
    catch (e: any) {
        console.log(e);

        const detail = e.response?.data?.message;

        if (detail) {
            error.value = detail;
        } else {
            error.value = "Unexpected error";
        }
    }
}


</script>

<template>
    <div class="p-8">
        <h2 class="text-2xl mb-4 font-thin">Create new branch</h2>
        <div class="border  border-primary-alt flex flex-col p-4 items-left gap-2 justify-center">
            <p class="font-bold text-sm">Title</p>
            <BaseInput v-model="title" class="bg-primary-alt w-100 mb-4"></BaseInput>

            <p class="font-bold text-sm">Parent branch</p>
            <select class="text-sm text-text-secondary rounded border border-primary-alt mb-4 bg-primary-alt"
                v-model="parent_id">
                <option :value="undefined">Root branch (no parent)</option>
                <option v-for="branch in all_branches" :key="branch.id" :value="branch.id">
                    {{ branch.title }}
                </option>
            </select>

            <p class="font-bold text-sm">Description</p>
            <BaseTextArea class="bg-primary-alt" v-model="description"></BaseTextArea>
            <p v-if="error" class="text-text-error">{{ error }}</p>
            <p v-if="success" class="text-accent">{{ success }}</p>
            <BaseButton class="w-70" @click="handle_create">
                Create
            </BaseButton>
        </div>
    </div>
</template>
