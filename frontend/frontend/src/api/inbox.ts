import { apiClient } from './client'
import { EmailItem, ThreadDetails } from '../types'

export const fetchEmails = async (searchOrParams?: string | Record<string, any>): Promise<EmailItem[]> => {
  const params = typeof searchOrParams === 'string' ? { q: searchOrParams } : searchOrParams
  const res = await apiClient.get('/emails', { params })
  const data = res.data

  if (Array.isArray(data)) return data
  if (data && typeof data === 'object' && Array.isArray((data as any).items)) return (data as any).items
  if (data && typeof data === 'object' && Array.isArray((data as any).results)) return (data as any).results

  return []
}

export const fetchThread = async (threadId: string): Promise<ThreadDetails> => {
  const res = await apiClient.get(`/threads/${encodeURIComponent(threadId)}`)
  return res.data
}

export const dryRunAgent = async (emailId: string) => {
  const res = await apiClient.post('/agents/dry-run', { emailId })
  return res.data
}

export const executeAgent = async (emailId: string) => {
  const res = await apiClient.post('/agents/execute', { emailId })
  return res.data
}

export const classifyEmail = async (emailId: string) => {
  const res = await apiClient.post(`/emails/${encodeURIComponent(emailId)}/classify`)
  return res.data
}
