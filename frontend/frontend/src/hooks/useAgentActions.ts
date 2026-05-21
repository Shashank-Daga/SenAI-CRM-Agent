import { useMutation, useQueryClient } from '@tanstack/react-query'
import { dryRunAgent, executeAgent, classifyEmail } from '../api/inbox'

export const useDryRunAgent = (emailId: string) => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => dryRunAgent(emailId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['thread', emailId] })
    },
  })
}

export const useExecuteAgent = (emailId: string) => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => executeAgent(emailId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['thread', emailId] })
      queryClient.invalidateQueries({ queryKey: ['inbox'] })
    },
  })
}

export const useClassifyEmail = (emailId: string) => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => classifyEmail(emailId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['thread', emailId] })
      queryClient.invalidateQueries({ queryKey: ['inbox'] })
    },
  })
}

export default useDryRunAgent
