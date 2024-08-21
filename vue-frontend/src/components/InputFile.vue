<template>
  <div class="items-center">
    <label class="bg-green-500 hover:bg-green-700 text-white p-1 px-4 rounded cursor-pointer">
      <span>{{ inputName }}</span>
      <input :id="id" type="file" class="hidden" @change="handleFileChange" :value="modelValue" />
    </label>
    <span v-if="selectedFile">
      {{ selectedFile.name }}
    </span>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const { inputName, id } = defineProps(['inputName', 'id'])
const emits = defineEmits(['update:modelValue'])

const selectedFile = ref('')
const handleFileChange = (event) => {
  selectedFile.value = event.target.file[0]
  emits('update:modelValue', selectedFile.value)
}
</script>
