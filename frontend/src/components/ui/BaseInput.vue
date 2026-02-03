<script setup lang="ts">
import { computed } from 'vue';
import { twMerge } from 'tailwind-merge';

interface Props {
  modelValue?: string;
  type?: string;
  placeholder?: string;
  disabled?: boolean;
  error?: boolean;
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  disabled: false,
  error: false,
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
}>();

const inputClasses = computed(() => {
  return twMerge(
    'p-2 rounded border transition-colors duration-200',
    'focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent',
    !props.error && !props.disabled ? 'border-primary-alt bg-surface-alt' : '',
    props.error ? 'border-error bg-error/5' : '',
    props.disabled ? 'border-gray-300 bg-gray-100 cursor-not-allowed text-gray-500' : '',
    props.class
  );
});

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.value);
};
</script>

<template>
  <input :type="type" :placeholder="placeholder" :disabled="disabled" :class="inputClasses" :value="modelValue"
    @input="handleInput" />
</template>