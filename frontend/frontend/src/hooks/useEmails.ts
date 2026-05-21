import { useQuery } from '@tanstack/react-query'
import { fetchEmails } from '../api/inbox'
import { EmailItem } from '../types'

export const useEmails = (search?: string) => {
  return useQuery<EmailItem[], Error>({
    queryKey: ['emails', search],
    queryFn: () => fetchEmails(search),
    refetchInterval: 15000,
    staleTime: 10000,
  })
}
