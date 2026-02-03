<script setup lang="ts">
import { computed } from 'vue';
import { twMerge } from 'tailwind-merge';

interface Props {
    modelValue?: string;
    placeholder?: string;
    disabled?: boolean;
    error?: boolean;
    class?: string;
}

const props = withDefaults(defineProps<Props>(), {
    placeholder: '',
    disabled: false,
    error: false,
});

const emit = defineEmits<{
    'update:modelValue': [value: string];
}>();

const textAreaClasses = computed(() => {
    return twMerge(
        'w-full h-80 p-2 rounded border transition-colors duration-200',
        'focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
        !props.error && !props.disabled ? 'border-primary-alt bg-surface-alt' : '',
        props.error ? 'border-error bg-error/5' : '',
        props.disabled ? 'border-gray-300 bg-gray-100 cursor-not-allowed text-gray-500' : '',
        props.class
    );
});

const handleInput = (event: Event) => {
    const target = event.target as HTMLTextAreaElement; // Здесь тип TextArea
    emit('update:modelValue', target.value);
};
</script>

<template>
    <textarea :placeholder="placeholder" :disabled="disabled" :class="textAreaClasses" :value="modelValue"
        @input="handleInput" />
</template>