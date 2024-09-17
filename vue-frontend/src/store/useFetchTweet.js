import { ref } from 'vue'
import { defineStore } from 'pinia'
import axiosInstance from '@/service/axiosInstance'

export const useTweet = defineStore('tweets', () => {
  const tweets = ref([])
  const status = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchTweets = async (url) => {
    loading.value = true
    error.value = null

    if (!url || typeof url !== 'string') {
      error.value = 'Invalid URL provided'
      console.error('Error fetching tweets: Invalid URL', url)
      loading.value = false
      return { success: false, error: error.value }
    }

    try {
      const response = await axiosInstance.get(url)
      status.value = response.status
      tweets.value = response.data.data
      loading.value = false
      return {
        success: true,
        data: response.data
      }
    } catch (e) {
      if (e.isAxiosError) {
        error.value = e.response?.data?.message || e.message
        console.error('Axios error fetching tweets:', e.message, e.response?.data)
      } else {
        error.value = 'An unexpected error occurred'
        console.error('Unexpected error fetching tweets:', e)
      }
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  return {
    tweets,
    loading,
    error,
    fetchTweets
  }
})
