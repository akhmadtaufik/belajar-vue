<template>
  <div class="items-center">
    <label class="bg-green-500 hover:bg-green-700 text-white p-1 px-4 rounded cursor-pointer">
      <span>{{ inputName }}</span>
      <input :id="id" type="file" class="hidden" @change="handleFileChange" />
    </label>
    <span v-if="selectedFile">
      {{ selectedFile.name }}
    </span>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue'

const props = defineProps({
  inputName: {
    type: String,
    required: true
  },
  id: {
    type: String,
    required: true
  },
  modelValue: {
    type: [File, null],
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const selectedFile = ref(props.modelValue)

const handleFileChange = (event) => {
  const file = event.target.files ? event.target.files[0] : null
  selectedFile.value = file
  emit('update:modelValue', file)
}

watch(
  () => props.modelValue,
  (newValue) => {
    selectedFile.value = newValue
  }
)
</script>
