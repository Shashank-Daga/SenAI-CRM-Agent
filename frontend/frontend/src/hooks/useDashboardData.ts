import { useQuery } from '@tanstack/react-query'
import { fetchDashboardOverview } from '../api/dashboard'
import { DashboardOverview } from '../types'

export const useDashboardData = () => {
  return useQuery<DashboardOverview, Error>({
    queryKey: ['dashboardOverview'],
    queryFn: () => fetchDashboardOverview(),
    staleTime: 20000,
    refetchInterval: 30000,
  })
}

export default useDashboardData
