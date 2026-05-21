import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  timeout: 15000,
})

// Attach a simple auth token handler
let authToken: string | null = null

export const setAuthToken = (token: string | null) => {
  authToken = token
  if (token) apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
  else delete apiClient.defaults.headers.common['Authorization']
}

// Response interceptor to normalize errors
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    const defaultError = { success: false, message: 'Network error', details: null }
    if (err.response && err.response.data) return Promise.reject(err.response.data)
    return Promise.reject(defaultError)
  },
)

export interface ApiResponse<T> {
  data: T
  message?: string
}
