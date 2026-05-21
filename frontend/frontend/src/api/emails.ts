import { apiClient, ApiResponse } from './client'
import { DashboardOverview, EmailItem, ThreadDetails, SagencyAnalytics, RagContext } from '../types'

export const fetchEmails = async (query?: string): Promise<EmailItem[]> => {
  const response = await apiClient.get<ApiResponse<EmailItem[]>>('/emails', {
    params: { q: query },
  })
  return response.data.data
}

export const fetchThread = async (contactEmail: string): Promise<ThreadDetails> => {
  const response = await apiClient.get<ApiResponse<ThreadDetails>>(`/threads/${encodeURIComponent(contactEmail)}`)
  return response.data.data
}

export const fetchSentimentTrend = async (): Promise<SagencyAnalytics> => {
  const response = await apiClient.get<ApiResponse<SagencyAnalytics>>('/analytics/sentiment-trend')
  return response.data.data
}

export const fetchCategoryBreakdown = async (): Promise<SagencyAnalytics> => {
  const response = await apiClient.get<ApiResponse<SagencyAnalytics>>('/analytics/category-breakdown')
  return response.data.data
}

export const dryRunAgent = async (emailId: string): Promise<unknown> => {
  const response = await apiClient.post<ApiResponse<unknown>>(`/agent/dry-run/${encodeURIComponent(emailId)}`)
  return response.data.data
}

export const executeAgent = async (emailId: string): Promise<unknown> => {
  const response = await apiClient.post<ApiResponse<unknown>>(`/agent/execute/${encodeURIComponent(emailId)}`)
  return response.data.data
}

export const classifyEmail = async (emailId: string): Promise<unknown> => {
  const response = await apiClient.post<ApiResponse<unknown>>(`/classify/email/${encodeURIComponent(emailId)}`)
  return response.data.data
}

export const searchRag = async (query: string): Promise<RagContext[]> => {
  const response = await apiClient.get<ApiResponse<RagContext[]>>('/rag/search', {
    params: { q: query },
  })
  return response.data.data
}

export const fetchReputation = async (company: string): Promise<unknown> => {
  const response = await apiClient.get<ApiResponse<unknown>>('/intelligence/reputation', {
    params: { company },
  })
  return response.data.data
}

export const fetchDashboardOverview = async (): Promise<DashboardOverview> => {
  const [emails, sentimentData, categoryData] = await Promise.all([
    fetchEmails(),
    fetchSentimentTrend(),
    fetchCategoryBreakdown(),
  ])

  const total = emails.length
  const escalated = emails.filter((item) => item.escalation).length
  const needsHuman = emails.filter((item) => item.needs_human).length
  const autoReplied = emails.filter((item) => item.auto_replied).length

  const teamPerformance = [
    { team: 'Inbound', responseRate: 78, resolutionRate: 64, backlog: Math.max(0, escalated - 2) },
    { team: 'AI Ops', responseRate: 88, resolutionRate: 72, backlog: Math.max(0, needsHuman - 3) },
    { team: 'Service', responseRate: 82, resolutionRate: 69, backlog: autoReplied },
  ]

  return {
    sentimentTrend: sentimentData.sentimentTrend,
    categoryBreakdown: categoryData.categoryBreakdown,
    escalationMetrics: sentimentData.escalationMetrics ?? {
      escalated: Math.round((escalated / Math.max(total, 1)) * 100),
      resolved: 100 - Math.round((escalated / Math.max(total, 1)) * 100),
      humanReviewPct: Math.round((needsHuman / Math.max(total, 1)) * 100),
    },
    automationMetrics: sentimentData.automationMetrics ?? {
      autoReplyRate: Math.round((autoReplied / Math.max(total, 1)) * 100),
      dryRunCount: 0,
      executionCount: 0,
    },
    atRiskAccounts: sentimentData.atRiskAccounts ?? [],
    inboxVolume: {
      total,
      escalated,
      needsHuman,
      autoReplied,
    },
    teamPerformance,
  }
}
