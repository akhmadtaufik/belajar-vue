<template>
  <main class="flex justify-content flex-col items-center mt-10">
    <h1 class="text-2xl">Registration Page</h1>
    <Form class="p-5 border-2 shadow-md">
      <div class="flex flex-col">
        <label for="username">Username</label>
        <input
          type="text"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
          name="username"
          v-model="formData.username"
        />
      </div>
      <div class="flex flex-col">
        <label for="email">E-mail</label>
        <input
          type="email"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
          name="email"
          v-model="formData.email"
        />
      </div>
      <div class="flex flex-col">
        <label for="password">Password</label>
        <input
          type="password"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
          name="password"
          v-model="formData.password"
        />
      </div>
      <div class="flex flex-col">
        <label for="c_password">Confirm Password</label>
        <input
          type="password"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
          name="c_password"
          v-model="formData.confirm_password"
        />
      </div>
      <div class="flex flex-col">
        <label for="role">Role</label>
        <Listbox v-model="selectedRole">
          <ListboxButton class="border-b-4 border-green-600">{{ selectedRole.role }}</ListboxButton>
          <ListboxOptions class="bg-green-400 text-white">
            <ListboxOption
              v-for="role in roles"
              :key="role.id"
              :value="role"
              class="p-2 hover:bg-gray-200"
              v-model="formData.role"
            >
              {{ role.role }}
            </ListboxOption>
          </ListboxOptions>
        </Listbox>
      </div>
      <button
        type="submit"
        class="bg-green-400 p-2 rounded-md text-white w-full mt-5"
        @click="handleRegister"
      >
        Submit
      </button>
      <RouterLink to="/login" class="text-sm hover:text-green-400">Back To Login</RouterLink>
    </Form>
  </main>
</template>

<script setup>
import Form from '@/components/Form.vue'
import { ref, reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { useAuth } from '@/store/useAuth'

const { tryRegister } = useAuth()

const roles = [
  { id: 1, role: 'admin' },
  { id: 2, role: 'user' }
]

const selectedRole = ref(roles[0])

const router = useRouter()

const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  role: selectedRole.value.role
})

const handleRegister = async () => {
  const result = await tryRegister(import.meta.env.VITE_FLASK_URL + '/api/auth/register', formData)
  if (result.success) {
    router.push('/login')
  } else {
    console.error('Registration Failed: ', result.error)
  }
}
</script>
