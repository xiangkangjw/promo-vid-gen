export interface RestaurantInfo {
  restaurant_name: string
  address: string
  website: string
  phone: string
  rating: number
  reviews_count: number
  place_id: string
}

export interface MenuItem {
  name: string
  price: string
  description: string
}

export interface MenuCategory {
  category: string
  items: MenuItem[]
}

export interface VideoScene {
  text: string
  duration: number
  image_prompt: string
  voiceover_text: string
}

export interface ScriptData {
  script: string
  scenes: VideoScene[]
  total_duration: number
  style: string
}

export interface VideoMetadata {
  duration: number
  file_size: number
  resolution: string
}

export interface VideoGenerationRequest {
  google_maps_url: string
  style: 'luxury' | 'casual' | 'street_food'
  duration: number
}

export interface VideoGenerationResponse {
  task_id: string
  status: 'initiated' | 'processing' | 'completed' | 'failed'
  message: string
}

export interface VideoGenerationStatus {
  task_id: string
  status: 'processing' | 'completed' | 'failed'
  progress: number
  current_step?: string
  restaurant_info?: RestaurantInfo
  menu_data?: {
    menu: MenuCategory[]
    extraction_method: string
  }
  script_data?: ScriptData
  video_metadata?: VideoMetadata
  video_url?: string
  thumbnail_url?: string
  error?: string
}