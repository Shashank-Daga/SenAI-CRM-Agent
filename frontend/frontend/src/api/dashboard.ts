import { fetchDashboardOverview as fetchOverviewFromEmails } from './emails'
import { DashboardOverview } from '../types'

export const fetchDashboardOverview = async (): Promise<DashboardOverview> => {
  return fetchOverviewFromEmails()
}
