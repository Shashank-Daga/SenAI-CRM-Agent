import { useQuery } from '@tanstack/react-query'
import { fetchEmails } from '../api/inbox'
import { EmailItem } from '../types'

export const useInbox = (search?: string) => {
  return useQuery<EmailItem[], Error>({
    queryKey: ['inbox', search],
    queryFn: () => fetchEmails(search),
    staleTime: 15000,
    refetchInterval: 20000,
  })
}

export default useInbox
