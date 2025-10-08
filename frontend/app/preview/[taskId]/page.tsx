'use client'

import { useParams, useRouter } from 'next/navigation'
import { useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { VideoPlayer } from '@/components/video-player'
import { ProgressTracker } from '@/components/progress-tracker'
import { useVideoStatus, useDownloadVideo } from '@/hooks/use-video-generation'
import { useVideoStore } from '@/lib/store'
import { VideoGenerationStatus } from '@/types'

export default function PreviewPage() {
  const params = useParams()
  const router = useRouter()
  const taskId = params.taskId as string

  const { setCurrentTaskId } = useVideoStore()
  const { data: status, isLoading, error } = useVideoStatus(taskId) as {
    data: VideoGenerationStatus | undefined
    isLoading: boolean
    error: any
  }
  const downloadMutation = useDownloadVideo()

  // Set current task ID for the store
  useEffect(() => {
    if (taskId) {
      setCurrentTaskId(taskId)
    }
  }, [taskId, setCurrentTaskId])

  const handleDownload = () => {
    if (taskId) {
      downloadMutation.mutate(taskId)
    }
  }

  const handleRegenerate = () => {
    router.push('/generate')
  }

  const getVideoUrl = (taskId: string) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    return `${baseUrl}/api/download/${taskId}`
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20">
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center gap-4">
                <Button variant="ghost" size="sm" asChild>
                  <Link href="/generate">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back
                  </Link>
                </Button>
                <div className="flex items-center gap-2">
                  <div className="text-2xl">🎬</div>
                  <span className="font-bold text-xl">AI Promo Creator</span>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="max-w-4xl mx-auto">
            <div className="text-center">
              <p className="text-muted-foreground">Loading video status...</p>
            </div>
          </div>
        </main>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20">
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center gap-4">
                <Button variant="ghost" size="sm" asChild>
                  <Link href="/generate">
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back
                  </Link>
                </Button>
                <div className="flex items-center gap-2">
                  <div className="text-2xl">🎬</div>
                  <span className="font-bold text-xl">AI Promo Creator</span>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="max-w-4xl mx-auto">
            <div className="text-center">
              <p className="text-red-500">Error loading video: {error.message}</p>
              <Button onClick={handleRegenerate} className="mt-4">
                Try Again
              </Button>
            </div>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="sm" asChild>
                <Link href="/generate">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back
                </Link>
              </Button>
              <div className="flex items-center gap-2">
                <div className="text-2xl">🎬</div>
                <span className="font-bold text-xl">AI Promo Creator</span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">
              {status?.status === 'completed'
                ? 'Your Video is Ready!'
                : status?.status === 'processing'
                ? 'Generating Your Video...'
                : 'Video Status'
              }
            </h1>
            {status?.restaurant_info && (
              <p className="text-lg text-muted-foreground">
                {status.restaurant_info.restaurant_name}
              </p>
            )}
          </div>

          {/* Show progress tracker for processing or completed video player */}
          {status && (
            status.status === 'processing' ? (
              <ProgressTracker status={status} />
            ) : (
              <VideoPlayer
                status={status}
                videoUrl={status.status === 'completed' ? getVideoUrl(taskId) : null}
                onDownload={handleDownload}
                onRegenerate={handleRegenerate}
                isDownloading={downloadMutation.isPending}
              />
            )
          )}
        </div>
      </main>
    </div>
  )
}