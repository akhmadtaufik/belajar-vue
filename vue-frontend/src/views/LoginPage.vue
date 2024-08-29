<template>
  <main class="flex justify-content flex-col items-center mt-10">
    <h1 class="text-2xl">Login Page</h1>
    <Form class="p-5 border-2 shadow-md">
      <div class="flex flex-col">
        <label for="username">Username</label>
        <input
          type="text"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
        />
      </div>
      <div class="flex flex-col">
        <label for="password">Password</label>
        <input
          type="password"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
        />
      </div>
      <button type="submit" class="bg-green-400 p-2 rounded-md text-white w-full mt-5">
        Submit
      </button>
      <RouterLink to="/register" class="text-sm hover:text-green-400">Sign Up</RouterLink>
    </Form>
  </main>
</template>

<script setup>
import Form from '@/components/Form.vue'
import { RouterLink } from 'vue-router'
</script>
