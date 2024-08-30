<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <nav class="flex bg-green-400 h-10 items-center">
    <ul class="ml-20 text-white flex gap-10">
      <RouterLink
        to="/"
        class="hover:border-b-4 hover:border-green-500 p-1 rounded-sm"
        active-class="border-b-4 border-white"
        >Home</RouterLink
      >
      <RouterLink
        to="/about"
        class="hover:border-b-4 hover:border-green-500 p-1 rounded-sm"
        active-class="border-b-4 border-white"
        >About</RouterLink
      >
      <RouterLink
        to="/login"
        class="hover:border-b-4 hover:border-green-500 p-1 rounded-sm"
        @click="handleLogout"
        >Logout</RouterLink
      >
    </ul>
  </nav>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuth } from '@/store/useAuth'

const auth = useAuth()
const router = useRouter()

const handleLogout = async () => {
  const result = await auth.tryLogout(import.meta.env.VITE_FLASK_URL + '/api/auth/logout')
  if (result.success) {
    router.push('/login')
  } else {
    console.error('Logout Failed: ', result.error)
  }
}
</script>
