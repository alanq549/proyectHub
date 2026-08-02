<template>
    <div class="user-avatar" :class="sizeClass">
        <img :src="src" :alt="alt" />
    </div>
</template>


<script setup lang="ts">

import { computed } from 'vue'


const props = defineProps<{
    src: string
    alt?: string
    size?: 'sm' | 'md' | 'lg'
}>()


const sizeClass = computed(() => ({
    'avatar-sm': props.size === 'sm',
    'avatar-md': props.size === 'md',
    'avatar-lg': props.size === 'lg',
}))


</script>


<style scoped>
.user-avatar {
    border-radius: 50%;
    overflow: hidden;
    background: #fff;
}


.user-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}


.avatar-sm {
    width: 32px;
    height: 32px;
}


.avatar-md {
    width: 48px;
    height: 48px;
}


.avatar-lg {
    width: 96px;
    height: 96px;
    border: 4px solid var(--surface, #f7f9fb);
    box-shadow:
        0 10px 15px -3px rgba(0, 0, 0, .1);
}
</style>