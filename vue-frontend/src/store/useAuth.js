import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuth = defineStore('auth', () => {
  const status = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const accessToken = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)

  const setToken = (access, refresh) => {
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    accessToken.value = access
    refreshToken.value = refresh
  }

  const removeToken = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    accessToken.value = null
    refreshToken.value = null
  }

  const tryLogin = async (url, formData) => {
    loading.value = true
    try {
      const response = await axios.post(url, formData)
      const access = response.data.access_token
      const refresh = response.data.refresh_token

      setToken(access, refresh)

      status.value = response.status
      return {
        success: true,
        data: response.data
      }
    } catch (e) {
      error.value = e
      console.error('Login error:', error.value)
      return { success: false, error: e.message }
    } finally {
      loading.value = false
    }
  }

  const tryRegister = async (url, formData) => {
    loading.value = true
    try {
      const response = await axios.post(url, formData)
      status.value = response.status
      return {
        success: true,
        data: response
      }
    } catch (e) {
      error.value = e
      console.error(error.value)
      return {
        success: false,
        error: e.message
      }
    } finally {
      loading.value = false
    }
  }

  const tryLogout = async (url) => {
    loading.value = true
    try {
      const response = await axios.post(url, null, {
        headers: {
          Authorization: `Bearer ${accessToken.value}`
        }
      })
      status.value = response.status
      removeToken()
      return {
        success: true
      }
    } catch (e) {
      error.value = e
      console.error(error.value)
      return {
        success: false,
        error: e.message
      }
    } finally {
      loading.value = false
    }
  }

  return {
    status,
    loading,
    error,
    tryLogin,
    tryLogout,
    tryRegister
  }
})
