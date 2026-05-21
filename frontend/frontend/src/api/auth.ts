import { apiClient, setAuthToken } from './client'

export const login = async (email: string, password: string) => {
  const res = await apiClient.post('/auth/login', { email, password })
  const data = res.data
  if (data?.token) setAuthToken(data.token)
  return data
}

export const logout = async () => {
  setAuthToken(null)
}

export const refreshToken = async () => {
  const res = await apiClient.post('/auth/refresh')
  const data = res.data
  if (data?.token) setAuthToken(data.token)
  return data
}
