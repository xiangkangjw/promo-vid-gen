import {
  VideoGenerationRequest,
  VideoGenerationResponse,
  VideoGenerationStatus
} from '@/types'

class ApiClient {
  private baseUrl: string

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new ApiError(
          response.status,
          errorData.message || `HTTP ${response.status}: ${response.statusText}`,
          errorData
        )
      }

      return await response.json()
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }

      // Network or other errors
      throw new ApiError(
        0,
        error instanceof Error ? error.message : 'Network error occurred',
        { originalError: error }
      )
    }
  }

  // Generate video from Google Maps URL using AgentOS Workflow
  async generateVideo(data: VideoGenerationRequest): Promise<VideoGenerationResponse> {
    // Create a message for the video generation workflow
    const message = `Create a promotional video for this restaurant: ${data.google_maps_url}. Style: ${data.style}, Duration: ${data.duration} seconds.`

    // Use FormData for multipart/form-data instead of JSON
    const formData = new FormData()
    formData.append('message', message)

    // Add workflow-specific dependencies as JSON
    const dependencies = JSON.stringify({
      google_maps_url: data.google_maps_url,
      video_style: data.style,
      duration: data.duration
    })
    formData.append('dependencies', dependencies)

    const url = `${this.baseUrl}/workflows/video-generation/runs`

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header - let the browser set it for FormData
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new ApiError(
          response.status,
          errorData.message || `HTTP ${response.status}: ${response.statusText}`,
          errorData
        )
      }

      const result = await response.json()

      // Convert AgentOS response to expected format
      return {
        task_id: result.run_id,
        status: 'initiated',
        message: 'Video generation started'
      }
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }

      // Network or other errors
      throw new ApiError(
        0,
        error instanceof Error ? error.message : 'Network error occurred',
        { originalError: error }
      )
    }
  }

  // Get video generation status using AgentOS workflow run status
  async getVideoStatus(taskId: string): Promise<VideoGenerationStatus> {
    const response = await this.request<{
      run_id: string
      status: string
      messages: Array<{
        role: string
        content: string
        created_at: string
      }>
    }>(`/workflows/video-generation/runs/${taskId}`)

    // Parse the messages to extract progress and data
    const lastMessage = response.messages[response.messages.length - 1]

    // Convert AgentOS response to expected format
    return {
      task_id: taskId,
      status: this.mapAgentOSStatus(response.status),
      progress: this.calculateProgress(response.messages),
      current_step: this.extractCurrentStep(lastMessage?.content || ''),
      // TODO: Parse structured data from agent messages
      restaurant_info: undefined,
      menu_data: undefined,
      script_data: undefined,
      video_metadata: undefined,
      video_url: undefined,
      thumbnail_url: undefined
    }
  }

  private mapAgentOSStatus(agentOSStatus: string): 'processing' | 'completed' | 'failed' {
    switch (agentOSStatus.toLowerCase()) {
      case 'completed':
        return 'completed'
      case 'failed':
      case 'error':
        return 'failed'
      default:
        return 'processing'
    }
  }

  private calculateProgress(messages: Array<{ content: string }>): number {
    // Simple progress calculation based on message count
    // TODO: Implement more sophisticated progress tracking
    const stepKeywords = ['restaurant', 'menu', 'script', 'video']
    let progress = 0

    for (const message of messages) {
      const content = message.content.toLowerCase()
      for (const keyword of stepKeywords) {
        if (content.includes(keyword) && content.includes('complete')) {
          progress += 25
        }
      }
    }

    return Math.min(progress, 100)
  }

  private extractCurrentStep(content: string): string {
    // Extract current step from agent message
    if (content.includes('restaurant')) return 'Extracting restaurant data'
    if (content.includes('menu')) return 'Analyzing menu'
    if (content.includes('script')) return 'Generating script'
    if (content.includes('video')) return 'Creating video'
    return 'Processing'
  }

  // Download video (returns blob)
  async downloadVideo(taskId: string): Promise<Blob> {
    const url = `${this.baseUrl}/api/download/${taskId}`

    const response = await fetch(url)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new ApiError(
        response.status,
        errorData.message || 'Failed to download video',
        errorData
      )
    }

    return response.blob()
  }

  // Get video URL for preview
  getVideoUrl(taskId: string): string {
    return `${this.baseUrl}/api/download/${taskId}`
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.request<{ status: string; timestamp: string }>('/health')
  }
}

// Custom error class for API errors
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }

  get isNetworkError(): boolean {
    return this.status === 0
  }

  get isClientError(): boolean {
    return this.status >= 400 && this.status < 500
  }

  get isServerError(): boolean {
    return this.status >= 500
  }
}

// Export singleton instance
export const apiClient = new ApiClient()

// Utility functions for common error handling
export const getErrorMessage = (error: unknown): string => {
  if (error instanceof ApiError) {
    return error.message
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'An unexpected error occurred'
}

export const isRetryableError = (error: unknown): boolean => {
  if (error instanceof ApiError) {
    // Retry on network errors and 5xx server errors
    return error.isNetworkError || error.isServerError
  }

  return false
}