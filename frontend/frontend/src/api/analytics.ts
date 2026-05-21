import { apiClient } from './client'
import { CategorySegment, SentimentTrendPoint } from '../types'

export const fetchSentimentTrend = async (since?: string): Promise<SentimentTrendPoint[]> => {
  const res = await apiClient.get('/analytics/sentiment', { params: { since } })
  return res.data
}

export const fetchCategoryBreakdown = async (): Promise<CategorySegment[]> => {
  const res = await apiClient.get('/analytics/categories')
  return res.data
}

export const fetchEscalationMetrics = async () => {
  const res = await apiClient.get('/analytics/escalations')
  return res.data
}

export const fetchAutomationMetrics = async () => {
  const res = await apiClient.get('/analytics/automation')
  return res.data
}
