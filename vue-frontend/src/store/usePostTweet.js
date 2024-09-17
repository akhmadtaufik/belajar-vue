import { ref } from 'vue'
import { defineStore } from 'pinia'
import axiosInstance from '@/service/axiosInstance'

export const usePostTweet = defineStore('postTweet', () => {
  const loading = ref(false)
  const success = ref(false)
  const error = ref(null)
  const data = ref(null)

  const tryPosting = async (url, content) => {
    loading.value = true
    error.value = null
    try {
      if (!content || typeof content !== 'string' || content.trim() === '') {
        throw new Error('Tweet content cannot be empty')
      }
      const response = await axiosInstance.post(
        url,
        { content },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      )
      data.value = response.data.data
      success.value = true
      loading.value = false
      return { success: true, data: response.data }
    } catch (err) {
      console.error('Error posting tweet:', err)
      error.value = err.message || 'An error occurred while posting the tweet'
      loading.value = false
      return { success: false, error: error.value }
    }
  }

  const tryUpload = async (url, formData) => {
    loading.value = true
    error.value = null
    try {
      console.log('Uploading tweet with file:', formData)
      const response = await axiosInstance.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      // console.log('Upload response:', response)
      data.value = response.data.data
      success.value = true
      loading.value = false
      return { success: true, data: response.data }
    } catch (err) {
      console.error('Error uploading tweet with file:', err)
      console.error('Error response:', err.response)
      error.value = err.message || 'An error occurred while uploading the tweet'
      loading.value = false
      return { success: false, error: error.value }
    }
  }

  return {
    loading,
    success,
    error,
    data,
    tryPosting,
    tryUpload
  }
})
