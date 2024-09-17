<template>
  <div class="bg-white rounded-lg shadow-lg mb-10 mt-5 hover:scale-100">
    <!-- Card Body -->
    <div class="p-4">
      <p class="text-gray-400 font-bold text-2xl">
        {{ tweet }}
      </p>
      <img v-if="image" :src="image" alt="Tweet image" class="mt-2 max-w-full h-auto" />
    </div>

    <div>
      <button name="like" class="hover:bg-green-700 p-2 text-white rounded-md">Likes</button>
    </div>

    <div class="bg-gray-200 p-3 text-gray-400">
      <p>Tweet From {{ user }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps(['user', 'tweet', 'image'])
</script>
