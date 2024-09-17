<template>
  <label :for="id">{{ label }}</label>
  <textarea
    :id="id"
    :rows="rows"
    :value="modelValue"
    class="border-2 rounded-md border-green-400"
    @input="updateValue($event.target.value)"
  ></textarea>
</template>

<script setup>
defineProps(['label', 'id', 'modelValue', 'rows'])
const emit = defineEmits(['update:modelValue'])

function updateValue(value) {
  emit('update:modelValue', value)
}
</script>
