<template>
  <Dialog :open="isOpen" @close="setIsOpen">
    <DialogPanel>
      <DialogTitle>{{ modalTitle }}</DialogTitle>
      <DialogDescription>
        {{ modalDesc }}
      </DialogDescription>
      <slot> </slot>
      <button @click="setIsOpen(false)">Deactivate</button>
      <button @click="setIsOpen(false)">Cancel</button>
    </DialogPanel>
  </Dialog>
</template>

<script setup>
defineProps(['modalTitle', 'modalDesc'])
import { ref } from 'vue'
import { Dialog, DialogPanel, DialogTitle, DialogDescription } from '@headlessui/vue'

const isOpen = ref(true)

function setIsOpen(value) {
  isOpen.value = value
}
</script>
