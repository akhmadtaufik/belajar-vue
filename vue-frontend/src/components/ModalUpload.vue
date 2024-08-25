<template>
  <Dialog :open="showModal" @close="$emit('toggle-modal', false)">
    <div class="fixed inset-0 bg-black/30" aria-hidden="true">
      <div class="fixed inset-0 flex w-screen items-center justify-center p-4">
        <slot> </slot>
      </div>
    </div>
  </Dialog>
</template>

<script setup>
import { Dialog } from '@headlessui/vue'

defineProps(['modalTitle', 'modalDesc', 'showModal'])
defineEmits(['toggle-modal'])
</script>
