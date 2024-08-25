<template>
  <label :for="id">{{ label }}</label>
  <textarea
    :id="id"
    :rows="rows"
    :value="modelValue"
    class="border-2 rounded-md border-green-400"
    @input="$emit('update:modelValue')"
  ></textarea>
</template>

<script setup>
defineProps(['label', 'id', 'modelValue', 'rows'])
defineEmits(['update:modelValue'])
</script>
