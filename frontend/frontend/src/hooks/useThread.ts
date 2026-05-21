import { useQuery } from '@tanstack/react-query'
import { fetchThread } from '../api/inbox'
import { ThreadDetails } from '../types'

export const useThread = (contactEmail: string) => {
  return useQuery<ThreadDetails, Error>({
    queryKey: ['thread', contactEmail],
    queryFn: () => fetchThread(contactEmail),
    refetchInterval: 15000,
    enabled: Boolean(contactEmail),
  })
}
