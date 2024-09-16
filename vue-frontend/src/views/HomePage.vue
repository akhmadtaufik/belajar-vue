<template>
  <main class="flex flex-col justify-items-center items-center">
    <h1 class="text-2xl">Home Page</h1>
    <Form @submit.prevent="submitData">
      <div class="flex flex-col w-full">
        <div class="flex flex-col">
          <TextAreaLabel id="textArea-input" label="Tweet" v-model="tweet" rows="5" />
        </div>
        <div class="flex gap-5 mt-5">
          <button
            type="submit"
            :disabled="postTweetStore.loading || !tweet.trim()"
            class="bg-green-400 text-white p-2 rounded-md"
          >
            {{ postTweetStore.loading ? 'Posting...' : 'Submit' }}
          </button>
          <button @click="toggleModal(true)" class="border-black border-2 p-2 rounded-md">
            Upload File
          </button>
        </div>
      </div>
    </Form>

    <section class="w-1/2">
      <p class="text-2xl font-semibold mt-4">Tweets</p>
      <div v-if="tweetStore.loading">Loading tweets...</div>
      <div v-else-if="tweetStore.error">Error: {{ tweetStore.error }}</div>
      <div v-else>
        <Card
          v-for="item in tweetStore.tweets"
          :key="item.id"
          :user="item.user_id"
          :tweet="item.content"
          :image="item.image_path"
        />
      </div>
    </section>

    <Teleport to="body">
      <ModalUpload @toggle-modal="toggleModal" :show-modal="showModal">
        <Form @submit.prevent="submitData(true)">
          <DialogPanel>
            <DialogTitle>
              <h1 class="text-xl">Upload Tweet</h1>
            </DialogTitle>
            <div class="flex flex-col">
              <div class="flex flex-col">
                <InputFile id="uploadFile" inputName="Upload File" v-model="uploadedFile" />
              </div>
              <div class="flex flex-col">
                <TextAreaLabel id="textArea-input" label="tweet" v-model="tweet" rows="5" />
              </div>
              <div class="flex gap-5 mt-5">
                <button
                  type="submit"
                  :disabled="postTweetStore.loading"
                  class="bg-green-400 text-white p-2 rounded-md"
                >
                  {{ postTweetStore.loading ? 'Uploading...' : 'Submit' }}
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
import { usePostTweet } from '@/store/usePostTweet'

import { ref, onMounted } from 'vue'

import { DialogPanel, DialogTitle } from '@headlessui/vue'

const tweet = ref('')
const tweetStore = useTweet()
const postTweetStore = usePostTweet()
const { fetchTweets } = tweetStore

const showModal = ref(false)
const uploadedFile = ref(null)

function toggleModal(value) {
  showModal.value = value
  if (!value) {
    uploadedFile.value = null
    tweet.value = ''
  }
}

async function submitData(withFile = false) {
  const url = `${import.meta.env.VITE_FLASK_URL}/api/tweets`
  let result

  if (!tweet.value || !tweet.value.trim()) {
    console.error('Tweet content is empty')
    return
  }

  console.log('Submitting tweet:', tweet.value) // Debug log

  if (withFile && uploadedFile.value) {
    result = await postTweetStore.tryUpload(url, tweet.value, uploadedFile.value)
  } else {
    result = await postTweetStore.tryPosting(url, tweet.value)
  }

  if (result.success) {
    tweet.value = ''
    uploadedFile.value = null
    if (withFile) {
      toggleModal(false)
    }
    await fetchTweets()
  } else {
    console.error('Failed to post tweet:', result.error)
  }
}

onMounted(async () => {
  console.log('HomePage mounted, fetching tweets...')
  try {
    await fetchTweets(import.meta.env.VITE_FLASK_URL + '/api/tweets')
  } catch (e) {
    console.error('Error in HomePage onMounted:', e)
  }
})
</script>
