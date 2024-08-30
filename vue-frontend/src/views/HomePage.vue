<template>
  <main class="flex flex-col justify-items-center items-center">
    <h1 class="text-2xl">Home Page</h1>
    <Form>
      <div class="flex flex-col w-full">
        <div class="flex flex-col">
          <TextAreaLabel id="textArea-input" label="tweet" v-model="tweet" rows="5" />
        </div>
        <div class="flex gap-5 mt-5">
          <button @click="submitData" class="bg-green-400 text-white p-2 rounded-md">Submit</button>
          <button @click="toggleModal(true)" class="border-black border-2 p-2 rounded-md">
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
      <ModalUpload @toggle-modal="toggleModal" :show-modal="showModal">
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
                <TextAreaLabel id="textArea-input" label="tweet" v-model="tweet" rows="5" />
              </div>
              <div class="flex gap-5 mt-5">
                <button @click="submitData" class="bg-green-400 text-white p-2 rounded-md">
                  Submit
                </button>
                <button @click="toggleModal(false)" class="border-black border-2 p-2 rounded-md">
                  Cancel
                </button>
              </div>
            </div>
          </DialogPanel>
        </Form>
      </ModalUpload>
    </Teleport>
  </main>
</template>

<script setup>
import Form from '@/components/Form.vue'
import Card from '@/components/Card.vue'
import InputFile from '@/components/InputFile.vue'
import TextAreaLabel from '@/components/TextAreaLabel.vue'
import ModalUpload from '@/components/ModalUpload.vue'
import { useTweet } from '@/store/useFetchTweet'

import { ref } from 'vue'

import { DialogPanel, DialogTitle } from '@headlessui/vue'

const tweet = ref('')

const { tweets } = useTweet()

const showModal = ref(false)

const uploadedFile = ref(null)

function toggleModal(value) {
  showModal.value = value
}
</script>
