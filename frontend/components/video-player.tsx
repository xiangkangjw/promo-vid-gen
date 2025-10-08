'use client'

import { useState, useRef } from 'react'
import { Download, Share2, RotateCcw, Play, Pause, Volume2, VolumeX, Maximize2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { VideoGenerationStatus } from '@/types'

interface VideoPlayerProps {
  status: VideoGenerationStatus
  videoUrl?: string | null
  onDownload?: () => void
  onRegenerate?: () => void
  isDownloading?: boolean
  className?: string
}

export function VideoPlayer({
  status,
  videoUrl,
  onDownload,
  onRegenerate,
  isDownloading = false,
  className
}: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [showShareMenu, setShowShareMenu] = useState(false)

  const handlePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const handleMuteToggle = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted
      setIsMuted(!isMuted)
    }
  }

  const handleFullscreen = () => {
    if (videoRef.current) {
      if (videoRef.current.requestFullscreen) {
        videoRef.current.requestFullscreen()
      }
    }
  }

  const handleShare = async (platform: string) => {
    if (!videoUrl) return

    const shareData = {
      title: `Check out this promo video for ${status.restaurant_info?.restaurant_name || 'this restaurant'}!`,
      text: 'Created with AI Promo Creator',
      url: videoUrl,
    }

    if (platform === 'native' && typeof navigator !== 'undefined' && 'share' in navigator) {
      try {
        await navigator.share(shareData)
      } catch (error) {
        console.log('Error sharing:', error)
      }
    } else {
      // Fallback: copy to clipboard
      try {
        if (typeof navigator !== 'undefined' && navigator.clipboard) {
          await navigator.clipboard.writeText(videoUrl)
          alert('Video URL copied to clipboard!')
        }
      } catch (error) {
        console.log('Error copying to clipboard:', error)
      }
    }

    setShowShareMenu(false)
  }

  if (status.status === 'failed') {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Video Generation Failed</CardTitle>
        </CardHeader>
        <CardContent>
          <Alert variant="destructive">
            <AlertDescription>
              {status.error || 'Something went wrong during video generation.'}
            </AlertDescription>
          </Alert>
          {onRegenerate && (
            <div className="mt-4">
              <Button onClick={onRegenerate} variant="outline">
                <RotateCcw className="w-4 h-4 mr-2" />
                Try Again
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    )
  }

  if (status.status !== 'completed' || !videoUrl) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Video Preview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
            <p className="text-muted-foreground">Video will appear here when generation is complete</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Your Video is Ready!</span>
          <Badge variant="secondary" className="bg-green-100 text-green-700">
            ✓ Completed
          </Badge>
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Video Player */}
        <div className="relative aspect-video bg-black rounded-lg overflow-hidden">
          <video
            ref={videoRef}
            src={videoUrl}
            className="w-full h-full object-contain"
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onEnded={() => setIsPlaying(false)}
          />

          {/* Video Controls Overlay */}
          <div className="absolute inset-0 bg-black/20 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
            <div className="flex items-center gap-2">
              <Button
                size="sm"
                variant="secondary"
                onClick={handlePlayPause}
                className="bg-white/80 hover:bg-white/90"
              >
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              </Button>
              <Button
                size="sm"
                variant="secondary"
                onClick={handleMuteToggle}
                className="bg-white/80 hover:bg-white/90"
              >
                {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
              </Button>
              <Button
                size="sm"
                variant="secondary"
                onClick={handleFullscreen}
                className="bg-white/80 hover:bg-white/90"
              >
                <Maximize2 className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Video Information */}
        {status.restaurant_info && (
          <div className="space-y-2">
            <h3 className="font-medium">{status.restaurant_info.restaurant_name}</h3>
            <p className="text-sm text-muted-foreground">{status.restaurant_info.address}</p>
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              {status.script_data && (
                <>
                  <span>Style: {status.script_data.style}</span>
                  <span>Duration: {status.script_data.total_duration}s</span>
                </>
              )}
              {status.video_metadata && (
                <span>Quality: {status.video_metadata.resolution}</span>
              )}
            </div>
          </div>
        )}

        <Separator />

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Download Button */}
          <Button
            onClick={onDownload}
            disabled={isDownloading}
            className="flex-1"
          >
            {isDownloading ? (
              <>
                <Download className="w-4 h-4 mr-2 animate-pulse" />
                Downloading...
              </>
            ) : (
              <>
                <Download className="w-4 h-4 mr-2" />
                Download Video
              </>
            )}
          </Button>

          {/* Share Button */}
          <div className="relative">
            <Button
              variant="outline"
              onClick={() => setShowShareMenu(!showShareMenu)}
              className="flex-1 sm:flex-none"
            >
              <Share2 className="w-4 h-4 mr-2" />
              Share
            </Button>

            {/* Share Menu */}
            {showShareMenu && (
              <div className="absolute top-full left-0 mt-2 w-48 bg-background border rounded-lg shadow-lg z-10">
                <div className="p-2 space-y-1">
                  {typeof navigator !== 'undefined' && 'share' in navigator && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="w-full justify-start"
                      onClick={() => handleShare('native')}
                    >
                      Share via...
                    </Button>
                  )}
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full justify-start"
                    onClick={() => handleShare('copy')}
                  >
                    Copy Link
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* Regenerate Button */}
          {onRegenerate && (
            <Button
              variant="outline"
              onClick={onRegenerate}
              className="flex-1 sm:flex-none"
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              Regenerate
            </Button>
          )}
        </div>

        {/* Download Options */}
        <div className="bg-muted/50 rounded-lg p-4">
          <h4 className="font-medium mb-2">Download Options</h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-sm">
            <div className="flex justify-between">
              <span>Format:</span>
              <span className="font-medium">MP4</span>
            </div>
            {status.video_metadata && (
              <>
                <div className="flex justify-between">
                  <span>Resolution:</span>
                  <span className="font-medium">{status.video_metadata.resolution}</span>
                </div>
                <div className="flex justify-between">
                  <span>Size:</span>
                  <span className="font-medium">
                    {(status.video_metadata.file_size / (1024 * 1024)).toFixed(1)} MB
                  </span>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Usage Tips */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-medium text-blue-900 mb-2">💡 Tips for Best Results</h4>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Perfect for Instagram, TikTok, and Facebook posts</li>
            <li>• Upload directly to your social media platforms</li>
            <li>• Add your own captions or hashtags for better engagement</li>
            <li>• Consider posting during peak hours for maximum reach</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  )
}