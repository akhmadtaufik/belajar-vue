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
        />
      </div>
      <div class="flex flex-col">
        <label for="email">E-mail</label>
        <input
          type="email"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
          name="email"
        />
      </div>
      <div class="flex flex-col">
        <label for="password">Password</label>
        <input
          type="password"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
          name="password"
        />
      </div>
      <div class="flex flex-col">
        <label for="c_password">Confirm Password</label>
        <input
          type="password"
          class="border-b-4 border-green-600 h-10 focus:outline-none focus:border-green-200"
          name="c_password"
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
            >
              {{ role.role }}
            </ListboxOption>
          </ListboxOptions>
        </Listbox>
      </div>
      <button type="submit" class="bg-green-400 p-2 rounded-md text-white w-full mt-5">
        Submit
      </button>
      <RouterLink to="/login" class="text-sm hover:text-green-400">Back To Login</RouterLink>
    </Form>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import Form from '@/components/Form.vue'
import { RouterLink } from 'vue-router'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'

const roles = [
  { id: 1, role: 'admin' },
  { id: 2, role: 'user' }
]

const selectedRole = ref(roles[0])
</script>
