<script setup lang="ts">
import type { BranchCreateDTO, BranchDTO } from "../api/dto";
import { ref } from "vue";
import { create_branch } from "../api/endpoints";

const title = ref<string>('');
const description = ref<string>('');
const error = ref<string>('');
const success = ref<string>('');

async function handle_create() {
    try {
        error.value = '';
        success.value = '';
        const new_branch: BranchCreateDTO = {
            title: title.value,
            description: description.value,
        }
        let created_branch = await create_branch(new_branch);
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
            <input type="text" v-model="title"
                class="w-100 p-1 mb-4 rounded border border-primary-alt  bg-primary-alt" />

            <p class="font-bold text-sm">Description</p>
            <textarea type="text" v-model="description"
                class="w-full  h-100 resize-none p-1 rounded border border-primary-alt  bg-primary-alt" />
            <p v-if="error" class="text-text-error">{{ error }}</p>
            <p v-if="success" class="text-accent">{{ success }}</p>
            <button @click="handle_create"
                class="w-60 h-10 m-2 cursor-pointer rounded border border-primary-alt bg-primary-alt">Create</button>
        </div>
    </div>
</template>
