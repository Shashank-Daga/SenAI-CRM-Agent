import { apiClient } from './client'

export const fetchCurrentUser = async () => {
  const res = await apiClient.get('/users/me')
  return res.data
}

export const fetchUsers = async (params?: Record<string, any>) => {
  const res = await apiClient.get('/users', { params })
  return res.data
}
