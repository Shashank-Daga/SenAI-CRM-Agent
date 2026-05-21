import { useQuery } from '@tanstack/react-query'
import { fetchSentimentTrend, fetchCategoryBreakdown, fetchEscalationMetrics, fetchAutomationMetrics } from '../api/analytics'
import { SagencyAnalytics } from '../types'

export const useAnalytics = () => {
  return useQuery<SagencyAnalytics, Error>({
    queryKey: ['analytics'],
    queryFn: async () => {
      const [sentimentTrend, categoryBreakdown, escalationMetrics, automationMetrics] = await Promise.all([
        fetchSentimentTrend(),
        fetchCategoryBreakdown(),
        fetchEscalationMetrics(),
        fetchAutomationMetrics(),
      ])

      return {
        sentimentTrend: sentimentTrend as any,
        categoryBreakdown: categoryBreakdown as any,
        escalationMetrics: escalationMetrics ?? undefined,
        automationMetrics: automationMetrics ?? undefined,
        atRiskAccounts: [],
      }
    },
    refetchInterval: 30000,
    staleTime: 20000,
  })
}
