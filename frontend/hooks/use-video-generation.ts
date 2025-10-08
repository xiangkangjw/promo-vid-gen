import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiClient, getErrorMessage } from '@/lib/api-client'
import { useVideoStore } from '@/lib/store'
import { VideoGenerationRequest, VideoGenerationStatus } from '@/types'

// Hook for generating videos
export function useGenerateVideo() {
  const queryClient = useQueryClient()
  const { setCurrentTaskId, setGenerationStatus, setIsGenerating, setError } = useVideoStore()

  return useMutation({
    mutationFn: (data: VideoGenerationRequest) => apiClient.generateVideo(data),
    onMutate: () => {
      setIsGenerating(true)
      setGenerationStatus('processing')
      setError(null)
    },
    onSuccess: (response) => {
      setCurrentTaskId(response.task_id)
      // Invalidate status queries to start polling
      queryClient.invalidateQueries({
        queryKey: ['video-status', response.task_id]
      })
    },
    onError: (error) => {
      setGenerationStatus('failed')
      setIsGenerating(false)
      setError(getErrorMessage(error))
    },
  })
}

// Hook for getting video status with polling
export function useVideoStatus(taskId: string | null, enabled = true) {
  const { setGenerationStatus, setIsGenerating } = useVideoStore()

  return useQuery<VideoGenerationStatus>({
    queryKey: ['video-status', taskId],
    queryFn: () => apiClient.getVideoStatus(taskId!),
    enabled: enabled && !!taskId,
    refetchInterval: (query) => {
      // Stop polling if video is completed or failed
      if (query.state.data?.status === 'completed' || query.state.data?.status === 'failed') {
        return false
      }
      // Poll every 2 seconds while processing
      return 2000
    },
  })
}

// Hook for downloading videos
export function useDownloadVideo() {
  return useMutation({
    mutationFn: (taskId: string) => apiClient.downloadVideo(taskId),
    onSuccess: (blob, taskId) => {
      // Create download link
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `promo-video-${taskId}.mp4`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    },
  })
}

// Hook for getting video URL for preview
export function useVideoUrl(taskId: string | null) {
  if (!taskId) return null
  return apiClient.getVideoUrl(taskId)
}

// Combined hook for the complete video generation workflow
export function useVideoWorkflow() {
  const {
    currentTaskId,
    generationStatus,
    isGenerating,
    error,
    setCurrentTaskId,
    resetState,
  } = useVideoStore()

  const generateMutation = useGenerateVideo()
  const statusQuery = useVideoStatus(currentTaskId, isGenerating)
  const downloadMutation = useDownloadVideo()

  const startGeneration = (data: VideoGenerationRequest) => {
    resetState()
    generateMutation.mutate(data)
  }

  const downloadVideo = () => {
    if (currentTaskId) {
      downloadMutation.mutate(currentTaskId)
    }
  }

  const resetWorkflow = () => {
    setCurrentTaskId(null)
    resetState()
  }

  return {
    // State
    currentTaskId,
    generationStatus,
    isGenerating,
    error,
    progress: statusQuery.data?.progress || 0,
    currentStep: statusQuery.data?.current_step,
    restaurantInfo: statusQuery.data?.restaurant_info,
    videoData: statusQuery.data as VideoGenerationStatus | undefined,

    // Actions
    startGeneration,
    downloadVideo,
    resetWorkflow,

    // Loading states
    isStarting: generateMutation.isPending,
    isDownloading: downloadMutation.isPending,

    // Video URL for preview
    videoUrl: useVideoUrl(currentTaskId),
  }
}