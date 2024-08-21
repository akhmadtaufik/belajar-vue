<template>
  <Navbar />
  <main class="flex flex-col justify-items-center items-center">
    <h1 class="text-2xl">Home Page</h1>
    <Form>
      <div class="flex flex-col w-full">
        <div class="flex flex-col">
          <label for="tweet">Tweet</label>
          <textarea
            rows="5"
            cols="10"
            v-model="tweet"
            class="border-2 rounded-md border-green-400"
          ></textarea>
        </div>
        <div class="flex gap-5 mt-5">
          <button @click="submitData" class="bg-green-400 text-white p-2 rounded-md">Submit</button>
          <button @click="setIsOpen(true)" class="border-black border-2 p-2 rounded-md">
            Upload File
          </button>
        </div>
      </div>
    </Form>

    <section class="w-1/2">
      <p class="text-2xl font-semibold mt-4">Tweets</p>
      <Card v-for="item in tweets" :key="item.user" :user="item.user" :tweet="item.tweet" />
    </section>

    <Teleport to="body">
      <Dialog :open="isOpen" @close="setIsOpen">
        <div class="fixed inset-0 bg-black/30 rounded-md" aria-hidden="true">
          <div class="fixed inset-0 flex w-screen items-center justify-center p-4">
            <Form>
              <DialogPanel>
                <DialogTitle>
                  <h1 class="text-xl">Upload Tweet</h1>
                </DialogTitle>
                <div class="flex flex-col">
                  <div class="flex flex-col">
                    <inputFile id="uploadFile" inputName="Upload File" v-model="uploadedFile" />
                  </div>
                  <div class="flex flex-col">
                    <label for="tweet">Tweet</label>
                    <textarea
                      rows="5"
                      cols="50"
                      id="tweet-modal"
                      v-model="tweet"
                      class="border-2 rounded-md border-green-400"
                    ></textarea>
                  </div>
                  <div class="flex gap-5 mt-5">
                    <button @click="submitData" class="bg-green-400 text-white p-2 rounded-md">
                      Submit
                    </button>
                    <button @click="setIsOpen(false)" class="border-black border-2 p-2 rounded-md">
                      Cancel
                    </button>
                  </div>
                </div>
              </DialogPanel>
            </Form>
          </div>
        </div>
      </Dialog>
    </Teleport>
  </main>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Form from '@/components/Form.vue'
import Card from '@/components/Card.vue'
import InputFile from '@/components/InputFile.vue'

import { ref } from 'vue'

import { Dialog, DialogPanel, DialogTitle } from '@headlessui/vue'

const tweet = ref('')

const tweets = [
  {
    user: 'user_1',
    tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
  },
  {
    user: 'user_2',
    tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
  },
  {
    user: 'user_3',
    tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
  },
  {
    user: 'user_4',
    tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
  },
  {
    user: 'user_5',
    tweet: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta, praesentium?'
  }
]

const isOpen = ref(false)

const uploadedFile = ref(null)

function setIsOpen(value) {
  isOpen.value = value
}
</script>
