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
      // console.log('Posting tweet:', { content })
      if (!content || content.trim() === '') {
        throw new Error('Tweet content cannot be empty')
      }
      const response = await axiosInstance.post(url, { content })
      // console.log('Response:', response)
      data.value = response.data.data
      success.value = response.data.success
      loading.value = false
      return { success: true, data: response.data }
    } catch (err) {
      console.error('Error details:', err.response?.data || err.message) // More detailed error logging
      error.value = err.response?.data?.error || err.message
      console.error('Error posting tweet:', error.value)
      loading.value = false
      return { success: false, error: error.value }
    }
  }

  const tryUpload = async (url, content, file) => {
    loading.value = true
    error.value = null
    try {
      const formData = new FormData()
      formData.append('content', content)
      if (file) {
        formData.append('file', file)
      }
      const response = await axiosInstance.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      data.value = response.data.data
      success.value = response.data.success
      loading.value = false
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err
      console.error('Error uploading tweet with file:', err)
      loading.value = false
      return { success: false, error: err.message }
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
