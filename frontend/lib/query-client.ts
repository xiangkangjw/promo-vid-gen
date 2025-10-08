import { QueryClient } from '@tanstack/react-query'
import { isRetryableError } from './api-client'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Stale time: 5 minutes
      staleTime: 1000 * 60 * 5,
      // Cache time: 10 minutes (cacheTime renamed to gcTime in v5)
      gcTime: 1000 * 60 * 10,
      // Retry logic
      retry: (failureCount, error) => {
        // Don't retry more than 3 times
        if (failureCount >= 3) return false

        // Only retry on retryable errors
        return isRetryableError(error)
      },
      // Retry delay with exponential backoff
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      // Don't refetch on window focus by default
      refetchOnWindowFocus: false,
    },
    mutations: {
      // Retry failed mutations once
      retry: 1,
      retryDelay: 1000,
    },
  },
})