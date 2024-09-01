import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useTweet = defineStore('tweets', () => {
  const tweets = ref([])
  const status = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const accessToken = ref(localStorage.getItem('access_token') || null)

  const fetchTweets = async (url) => {
    loading.value = true
    try {
      const response = await axios.get(url, {
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      })
      status.value = response.status
      tweets.value = response.data.data
      loading.value = false
      return {
        success: true,
        data: response.data
      }
    } catch (e) {
      error.value = e.response?.data?.message || e.message
      console.error('Error fetching tweets:', e)
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
