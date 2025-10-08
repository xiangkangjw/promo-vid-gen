'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { VideoGenerator } from '@/components/video-generator'
import { ProgressTracker } from '@/components/progress-tracker'
import { useVideoWorkflow } from '@/hooks/use-video-generation'

export default function GeneratePage() {
  const router = useRouter()
  const {
    isGenerating,
    generationStatus,
    currentTaskId,
    videoData
  } = useVideoWorkflow()

  // Redirect to preview page when video is completed
  useEffect(() => {
    if (generationStatus === 'completed' && currentTaskId) {
      router.push(`/preview/${currentTaskId}`)
    }
  }, [generationStatus, currentTaskId, router])

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="sm" asChild>
                <Link href="/">
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
        <div className="max-w-2xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">
              {isGenerating ? 'Generating Your Video' : 'Generate Your Video'}
            </h1>
            <p className="text-lg text-muted-foreground">
              {isGenerating
                ? 'Please wait while we create your promotional video'
                : 'Enter your restaurant\'s Google Maps URL and let AI create a professional promotional video'
              }
            </p>
          </div>

          {/* Show generator form or progress tracker */}
          {isGenerating && videoData && currentTaskId ? (
            <ProgressTracker status={videoData} />
          ) : (
            <VideoGenerator />
          )}
        </div>
      </main>
    </div>
  )
}