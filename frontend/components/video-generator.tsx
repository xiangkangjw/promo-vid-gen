'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { MapPin, Clock, Palette, Loader2 } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'

import { useVideoWorkflow } from '@/hooks/use-video-generation'
import { VideoGenerationRequest } from '@/types'

// Form validation schema
const videoGenerationSchema = z.object({
  googleMapsUrl: z
    .string()
    .min(1, 'Google Maps URL is required')
    .url('Must be a valid URL')
    .refine(
      (url) => {
        const googleMapsPatterns = [
          /maps\.google\.com/,
          /goo\.gl\/maps/,
          /maps\.app\.goo\.gl/,
        ]
        return googleMapsPatterns.some(pattern => pattern.test(url))
      },
      'Must be a Google Maps URL'
    ),
  style: z.enum(['luxury', 'casual', 'street_food']),
  duration: z.number().min(15).max(60),
})

type VideoGenerationForm = z.infer<typeof videoGenerationSchema>

const styleOptions = [
  {
    value: 'luxury' as const,
    label: 'Luxury',
    description: 'Elegant and sophisticated style for fine dining',
    color: 'bg-purple-100 text-purple-700 border-purple-200',
    example: 'Perfect for upscale restaurants'
  },
  {
    value: 'casual' as const,
    label: 'Casual',
    description: 'Friendly and welcoming style for everyday dining',
    color: 'bg-blue-100 text-blue-700 border-blue-200',
    example: 'Great for family restaurants'
  },
  {
    value: 'street_food' as const,
    label: 'Street Food',
    description: 'Vibrant and energetic style for quick service',
    color: 'bg-orange-100 text-orange-700 border-orange-200',
    example: 'Ideal for food trucks & quick bites'
  }
]

const durationOptions = [
  { value: 15, label: '15 seconds', description: 'Quick social media snippet' },
  { value: 30, label: '30 seconds', description: 'Standard promotional video' },
  { value: 60, label: '60 seconds', description: 'Detailed showcase' }
]

export function VideoGenerator() {
  const router = useRouter()
  const { startGeneration, isStarting, error } = useVideoWorkflow()
  const [selectedStyle, setSelectedStyle] = useState<'luxury' | 'casual' | 'street_food'>('casual')

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    setValue,
    watch,
  } = useForm<VideoGenerationForm>({
    resolver: zodResolver(videoGenerationSchema),
    defaultValues: {
      googleMapsUrl: '',
      style: 'casual',
      duration: 30,
    },
    mode: 'onChange',
  })

  const watchedValues = watch()

  const onSubmit = async (data: VideoGenerationForm) => {
    const request: VideoGenerationRequest = {
      google_maps_url: data.googleMapsUrl,
      style: data.style,
      duration: data.duration,
    }

    startGeneration(request)
  }

  const handleStyleSelect = (style: 'luxury' | 'casual' | 'street_food') => {
    setSelectedStyle(style)
    setValue('style', style, { shouldValidate: true })
  }

  const handleDurationSelect = (duration: number) => {
    setValue('duration', duration, { shouldValidate: true })
  }

  return (
    <div className="space-y-8">
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {/* URL Input Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="w-5 h-5 text-primary" />
              Restaurant URL
            </CardTitle>
            <CardDescription>
              Paste your restaurant's Google Maps URL below
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Input
                {...register('googleMapsUrl')}
                placeholder="https://maps.google.com/... or https://goo.gl/maps/..."
                className={errors.googleMapsUrl ? 'border-red-500' : ''}
              />
              {errors.googleMapsUrl && (
                <p className="text-sm text-red-500">{errors.googleMapsUrl.message}</p>
              )}
              <p className="text-xs text-muted-foreground">
                💡 Find your restaurant on Google Maps, click "Share", and copy the link
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Style Selection */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Palette className="w-5 h-5 text-primary" />
              Video Style
            </CardTitle>
            <CardDescription>
              Choose the style that best matches your restaurant's vibe
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {styleOptions.map((option) => (
                <div
                  key={option.value}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition-all hover:shadow-md ${
                    selectedStyle === option.value
                      ? 'border-primary bg-primary/5'
                      : 'border-border hover:border-primary/50'
                  }`}
                  onClick={() => handleStyleSelect(option.value)}
                >
                  <div className="flex flex-col items-center text-center space-y-2">
                    <Badge className={option.color}>
                      {option.label}
                    </Badge>
                    <h3 className="font-medium">{option.description}</h3>
                    <p className="text-xs text-muted-foreground">{option.example}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Duration Selection */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-primary" />
              Video Duration
            </CardTitle>
            <CardDescription>
              Select your preferred video length
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {durationOptions.map((option) => (
                <div
                  key={option.value}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition-all hover:shadow-md ${
                    watchedValues.duration === option.value
                      ? 'border-primary bg-primary/5'
                      : 'border-border hover:border-primary/50'
                  }`}
                  onClick={() => handleDurationSelect(option.value)}
                >
                  <div className="text-center space-y-1">
                    <h3 className="font-medium">{option.label}</h3>
                    <p className="text-sm text-muted-foreground">{option.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Generate Button */}
        <div className="flex justify-center">
          <Button
            type="submit"
            size="lg"
            disabled={!isValid || isStarting}
            className="min-w-48"
          >
            {isStarting ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Generating...
              </>
            ) : (
              'Generate Video'
            )}
          </Button>
        </div>
      </form>

      {/* Preview of selections */}
      {watchedValues.googleMapsUrl && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Generation Preview</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex items-center gap-2 text-sm">
              <MapPin className="w-4 h-4 text-muted-foreground" />
              <span className="truncate">{watchedValues.googleMapsUrl}</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <Palette className="w-4 h-4 text-muted-foreground" />
              <span>{styleOptions.find(s => s.value === watchedValues.style)?.label} style</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <Clock className="w-4 h-4 text-muted-foreground" />
              <span>{watchedValues.duration} seconds</span>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}