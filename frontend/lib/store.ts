import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { VideoGenerationStatus } from '@/types'

interface VideoGenerationState {
  // Current video generation
  currentTaskId: string | null
  generationStatus: 'idle' | 'processing' | 'completed' | 'failed'

  // UI state
  isGenerating: boolean
  showProgress: boolean

  // Error handling
  error: string | null

  // Actions
  setCurrentTaskId: (taskId: string | null) => void
  setGenerationStatus: (status: VideoGenerationState['generationStatus']) => void
  setIsGenerating: (isGenerating: boolean) => void
  setShowProgress: (showProgress: boolean) => void
  setError: (error: string | null) => void
  resetState: () => void
}

export const useVideoStore = create<VideoGenerationState>()(
  devtools(
    (set) => ({
      // Initial state
      currentTaskId: null,
      generationStatus: 'idle',
      isGenerating: false,
      showProgress: false,
      error: null,

      // Actions
      setCurrentTaskId: (taskId) =>
        set({ currentTaskId: taskId }, false, 'setCurrentTaskId'),

      setGenerationStatus: (status) =>
        set({ generationStatus: status }, false, 'setGenerationStatus'),

      setIsGenerating: (isGenerating) =>
        set({ isGenerating }, false, 'setIsGenerating'),

      setShowProgress: (showProgress) =>
        set({ showProgress }, false, 'setShowProgress'),

      setError: (error) =>
        set({ error }, false, 'setError'),

      resetState: () =>
        set(
          {
            currentTaskId: null,
            generationStatus: 'idle',
            isGenerating: false,
            showProgress: false,
            error: null,
          },
          false,
          'resetState'
        ),
    }),
    {
      name: 'video-store',
    }
  )
)

// Form state for video generation
interface VideoFormState {
  googleMapsUrl: string
  style: 'luxury' | 'casual' | 'street_food'
  duration: number

  // Form validation
  isValid: boolean
  isDirty: boolean

  // Actions
  setGoogleMapsUrl: (url: string) => void
  setStyle: (style: VideoFormState['style']) => void
  setDuration: (duration: number) => void
  setIsValid: (isValid: boolean) => void
  setIsDirty: (isDirty: boolean) => void
  resetForm: () => void
}

export const useVideoFormStore = create<VideoFormState>()(
  devtools(
    (set) => ({
      // Initial state
      googleMapsUrl: '',
      style: 'casual',
      duration: 30,
      isValid: false,
      isDirty: false,

      // Actions
      setGoogleMapsUrl: (url) =>
        set({ googleMapsUrl: url, isDirty: true }, false, 'setGoogleMapsUrl'),

      setStyle: (style) =>
        set({ style, isDirty: true }, false, 'setStyle'),

      setDuration: (duration) =>
        set({ duration, isDirty: true }, false, 'setDuration'),

      setIsValid: (isValid) =>
        set({ isValid }, false, 'setIsValid'),

      setIsDirty: (isDirty) =>
        set({ isDirty }, false, 'setIsDirty'),

      resetForm: () =>
        set(
          {
            googleMapsUrl: '',
            style: 'casual',
            duration: 30,
            isValid: false,
            isDirty: false,
          },
          false,
          'resetForm'
        ),
    }),
    {
      name: 'video-form-store',
    }
  )
)

// UI state for various components
interface UIState {
  // Navigation
  isMenuOpen: boolean

  // Modals and dialogs
  isErrorDialogOpen: boolean
  isSuccessDialogOpen: boolean

  // Loading states
  isPageLoading: boolean

  // Actions
  setIsMenuOpen: (isOpen: boolean) => void
  setIsErrorDialogOpen: (isOpen: boolean) => void
  setIsSuccessDialogOpen: (isOpen: boolean) => void
  setIsPageLoading: (isLoading: boolean) => void
}

export const useUIStore = create<UIState>()(
  devtools(
    (set) => ({
      // Initial state
      isMenuOpen: false,
      isErrorDialogOpen: false,
      isSuccessDialogOpen: false,
      isPageLoading: false,

      // Actions
      setIsMenuOpen: (isOpen) =>
        set({ isMenuOpen: isOpen }, false, 'setIsMenuOpen'),

      setIsErrorDialogOpen: (isOpen) =>
        set({ isErrorDialogOpen: isOpen }, false, 'setIsErrorDialogOpen'),

      setIsSuccessDialogOpen: (isOpen) =>
        set({ isSuccessDialogOpen: isOpen }, false, 'setIsSuccessDialogOpen'),

      setIsPageLoading: (isLoading) =>
        set({ isPageLoading: isLoading }, false, 'setIsPageLoading'),
    }),
    {
      name: 'ui-store',
    }
  )
)