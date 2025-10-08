'use client'

import { useEffect, useState } from 'react'
import { CheckCircle, Clock, Loader2, MapPin, FileText, Video, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { VideoGenerationStatus } from '@/types'

interface ProgressTrackerProps {
  status: VideoGenerationStatus
  className?: string
}

const steps = [
  {
    id: 'parsing_maps',
    label: 'Parse Google Maps',
    description: 'Extracting restaurant information',
    icon: MapPin,
  },
  {
    id: 'extracting_menu',
    label: 'Extract Menu',
    description: 'Finding menu items and details',
    icon: FileText,
  },
  {
    id: 'generating_script',
    label: 'Generate Script',
    description: 'Creating promotional content',
    icon: Video,
  },
  {
    id: 'creating_video',
    label: 'Create Video',
    description: 'Assembling final video',
    icon: Video,
  },
]

function getStepStatus(stepId: string, currentStep?: string, progress: number = 0): 'completed' | 'current' | 'pending' {
  const stepIndex = steps.findIndex(step => step.id === stepId)
  const currentStepIndex = currentStep ? steps.findIndex(step => step.id === currentStep) : -1

  if (stepIndex < currentStepIndex || (stepIndex === currentStepIndex && progress === 100)) {
    return 'completed'
  } else if (stepIndex === currentStepIndex) {
    return 'current'
  } else {
    return 'pending'
  }
}

function formatTimeRemaining(progress: number): string {
  if (progress === 0) return '3-5 minutes'
  if (progress < 25) return '2-4 minutes'
  if (progress < 50) return '1-3 minutes'
  if (progress < 75) return '1-2 minutes'
  if (progress < 95) return '< 1 minute'
  return 'Almost done'
}

export function ProgressTracker({ status, className }: ProgressTrackerProps) {
  const [elapsedTime, setElapsedTime] = useState(0)

  // Track elapsed time
  useEffect(() => {
    if (status.status === 'processing') {
      const interval = setInterval(() => {
        setElapsedTime(prev => prev + 1)
      }, 1000)

      return () => clearInterval(interval)
    }
  }, [status.status])

  const formatElapsedTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (status.status === 'failed') {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-destructive">
            <AlertCircle className="w-5 h-5" />
            Generation Failed
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Alert variant="destructive">
            <AlertDescription>
              {status.error || 'An error occurred during video generation. Please try again.'}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center gap-2">
            <Loader2 className="w-5 h-5 animate-spin text-primary" />
            Generating Your Video
          </span>
          <Badge variant="secondary">
            <Clock className="w-3 h-3 mr-1" />
            {formatElapsedTime(elapsedTime)}
          </Badge>
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Overall Progress */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Overall Progress</span>
            <span>{Math.round(status.progress || 0)}%</span>
          </div>
          <Progress value={status.progress || 0} className="h-2" />
          <p className="text-xs text-muted-foreground text-center">
            Estimated time remaining: {formatTimeRemaining(status.progress || 0)}
          </p>
        </div>

        {/* Step Progress */}
        <div className="space-y-4">
          {steps.map((step, index) => {
            const stepStatus = getStepStatus(step.id, status.current_step, status.progress)
            const Icon = step.icon

            return (
              <div key={step.id} className="flex items-center gap-4">
                {/* Step Icon */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center border-2 ${
                  stepStatus === 'completed'
                    ? 'bg-green-100 border-green-500 text-green-600'
                    : stepStatus === 'current'
                    ? 'bg-primary/10 border-primary text-primary'
                    : 'bg-muted border-muted-foreground/20 text-muted-foreground'
                }`}>
                  {stepStatus === 'completed' ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : stepStatus === 'current' ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Icon className="w-4 h-4" />
                  )}
                </div>

                {/* Step Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className={`font-medium ${
                      stepStatus === 'completed'
                        ? 'text-green-600'
                        : stepStatus === 'current'
                        ? 'text-primary'
                        : 'text-muted-foreground'
                    }`}>
                      {step.label}
                    </h3>
                    {stepStatus === 'completed' && (
                      <Badge variant="outline" className="text-xs border-green-500 text-green-600">
                        ✓ Done
                      </Badge>
                    )}
                    {stepStatus === 'current' && (
                      <Badge variant="outline" className="text-xs border-primary text-primary">
                        In progress
                      </Badge>
                    )}
                  </div>
                  <p className="text-sm text-muted-foreground">{step.description}</p>
                </div>
              </div>
            )
          })}
        </div>

        {/* Restaurant Info Preview */}
        {status.restaurant_info && (
          <div className="border-t pt-4 space-y-2">
            <h4 className="font-medium text-sm">Restaurant Information</h4>
            <div className="text-sm space-y-1">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-muted-foreground" />
                <span>{status.restaurant_info.restaurant_name}</span>
              </div>
              <p className="text-muted-foreground ml-6">{status.restaurant_info.address}</p>
              {status.restaurant_info.rating && (
                <p className="text-muted-foreground ml-6">
                  ⭐ {status.restaurant_info.rating} ({status.restaurant_info.reviews_count} reviews)
                </p>
              )}
            </div>
          </div>
        )}

        {/* Menu Data Preview */}
        {status.menu_data && (
          <div className="border-t pt-4 space-y-2">
            <h4 className="font-medium text-sm">Menu Extraction</h4>
            <div className="text-sm text-muted-foreground">
              <p>Found {status.menu_data.menu.length} menu categories</p>
              <p>Total items: {status.menu_data.menu.reduce((acc, cat) => acc + cat.items.length, 0)}</p>
              <p className="text-xs">Method: {status.menu_data.extraction_method}</p>
            </div>
          </div>
        )}

        {/* Script Data Preview */}
        {status.script_data && (
          <div className="border-t pt-4 space-y-2">
            <h4 className="font-medium text-sm">Script Generation</h4>
            <div className="text-sm text-muted-foreground">
              <p>Style: {status.script_data.style}</p>
              <p>Duration: {status.script_data.total_duration}s</p>
              <p>Scenes: {status.script_data.scenes.length}</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}