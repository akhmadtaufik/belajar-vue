<template>
  <h1>Hello World</h1>
</template>

<script setup>
import { onBeforeMount, onMounted, ref } from 'vue'

const fetchData = () => {
  console.log('fetching data...')
}

const data = ref({})

const calculateTotalData = () => {
  console.log('calculating total data...')
}

onBeforeMount(() => {
  const response = fetchData()
  data.value = response

  // console.log('Component before mount')
})

onMounted(() => {
  calculateTotalData()

  // console.log('Component mounted')
})
</script>
