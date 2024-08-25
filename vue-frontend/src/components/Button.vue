<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <button :type="buttonType" :class="className">{{ name }}</button>
</template>

<script setup>
defineProps({
  className: String,
  buttonType: String,
  name: {
    type: String,
    default: 'Submit'
  }
})
</script>
