<!-- eslint-disable vue/multi-word-component-names -->
<!-- eslint-disable vue/no-parsing-error -->
<template>
  <form action="#" @submit.prevent class="bg-white p-3 w-1/2 rounded-md" :class="class">
    <slot> </slot>
  </form>
</template>

<script setup>
defineProps(['class'])
</script>
