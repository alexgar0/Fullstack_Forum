<script setup lang="ts">
import { computed } from 'vue';
import { twMerge } from 'tailwind-merge';

const props = defineProps({
  class: String
});

const buttonClasses = computed(() => {
  return twMerge(
    'cursor-pointer rounded border border-primary-alt bg-primary-alt w-40 h-10',
    props.class
  );
});
</script>

<template>
  <button :className="buttonClasses">
    <slot />
  </button>
</template>