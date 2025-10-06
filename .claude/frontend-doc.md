# Frontend Design Document — AI Promo Creator

## 1. Overview

The frontend is a Next.js application that provides a simple, user-friendly interface for restaurant owners to generate promotional videos from Google Maps URLs.

## 2. Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** Shadcn/ui components
- **State Management:** React Query + Zustand
- **Forms:** React Hook Form + Zod validation
- **Deployment:** Vercel

## 3. User Journey

```
Landing Page → URL Input → Processing → Video Preview → Download/Share
```

### 3.1 Landing Page
- Hero section explaining the product
- Demo video showcasing the process
- Simple CTA: "Generate Your Video"
- Pricing information
- Examples of generated videos

### 3.2 Video Generation Flow
1. **URL Input Screen**
   - Large input field for Google Maps URL
   - Style selector (Luxury, Casual, Street Food)
   - Duration selector (15s, 30s, 60s)
   - "Generate Video" button

2. **Processing Screen**
   - Real-time progress indicator
   - Step-by-step status updates
   - Estimated time remaining
   - Preview of extracted restaurant info

3. **Preview & Download**
   - Video player with generated content
   - Download options (MP4, different resolutions)
   - Social sharing buttons
   - Regeneration options

## 4. Pages & Components

### 4.1 Page Structure
```
/                    # Landing page
/generate           # Video generation interface
/preview/[taskId]   # Video preview and download
/pricing            # Pricing tiers
/examples           # Sample videos
/about              # About the service
```

### 4.2 Key Components

#### VideoGenerator (`/components/VideoGenerator.tsx`)
- Main generation interface
- Handles URL input, style selection, API calls
- Progress tracking and status updates

#### VideoPlayer (`/components/VideoPlayer.tsx`)
- Custom video player with controls
- Download and sharing functionality
- Thumbnail generation

#### ProgressTracker (`/components/ProgressTracker.tsx`)
- Real-time generation progress
- Step indicators (Map Parse → Menu Extract → Script Generate → Video Create)
- Time estimates and status messages

#### StyleSelector (`/components/StyleSelector.tsx`)
- Visual style picker with previews
- Luxury, Casual, Street Food options
- Custom brand tone settings (future)

## 5. API Integration

### 5.1 Endpoints
```typescript
// Generate video
POST /api/generate-video
Body: { google_maps_url: string, style: string, duration: number }
Response: { task_id: string, status: string }

// Check status
GET /api/status/:taskId
Response: { status: string, progress: number, current_step: string }

// Download video
GET /api/download/:taskId
Response: File download or redirect to S3 URL
```

### 5.2 State Management
```typescript
interface VideoState {
  currentTask: string | null
  generationStatus: 'idle' | 'processing' | 'completed' | 'failed'
  progress: number
  restaurantInfo: RestaurantInfo | null
  videoUrl: string | null
  error: string | null
}
```

## 6. UI/UX Design

### 6.1 Design System
- **Primary Colors:** Modern blue gradient (#4F46E5 → #7C3AED)
- **Secondary:** Warm orange (#F59E0B) for CTAs
- **Neutral:** Gray scale for text and backgrounds
- **Typography:** Inter font family
- **Spacing:** 8px base unit system

### 6.2 Mobile-First Design
- Responsive design for mobile, tablet, desktop
- Touch-friendly interface
- Progressive enhancement

### 6.3 Key Screens Wireframes

#### Landing Page
```
┌─────────────────────────────────────┐
│            Navigation               │
├─────────────────────────────────────┤
│                                     │
│    🎬 AI Promo Creator              │
│                                     │
│    Generate restaurant videos       │
│    from Google Maps in minutes      │
│                                     │
│    [Start Creating →]               │
│                                     │
│    ┌───┐ ┌───┐ ┌───┐               │
│    │📱 │ │🍽️ │ │⬇️ │               │
│    │URL│ │Gen│ │DL │               │
│    └───┘ └───┘ └───┘               │
│                                     │
└─────────────────────────────────────┘
```

#### Generation Interface
```
┌─────────────────────────────────────┐
│ ◄ Back         AI Promo Creator     │
├─────────────────────────────────────┤
│                                     │
│  📍 Enter Google Maps URL           │
│  ┌─────────────────────────────────┐ │
│  │ https://maps.app.goo.gl/...    │ │
│  └─────────────────────────────────┘ │
│                                     │
│  🎨 Choose Style                    │
│  ┌─────┐ ┌─────┐ ┌─────┐           │
│  │Luxry│ │Casul│ │Strt │           │
│  │  ✓  │ │     │ │     │           │
│  └─────┘ └─────┘ └─────┘           │
│                                     │
│  ⏱️ Duration: [30s ▼]              │
│                                     │
│        [Generate Video →]           │
│                                     │
└─────────────────────────────────────┘
```

#### Processing Screen
```
┌─────────────────────────────────────┐
│           🎬 Generating...          │
├─────────────────────────────────────┤
│                                     │
│  ✅ 1. Parse Google Maps           │
│  ✅ 2. Extract Menu                │
│  🔄 3. Generate Script              │
│  ⏳ 4. Create Video                │
│                                     │
│  ████████░░ 75% Complete            │
│                                     │
│  📍 Oro Restaurant                  │
│  📄 Found 15 menu items             │
│  📝 Generating luxury script...     │
│                                     │
│  ⏱️ Estimated: 2 minutes           │
│                                     │
└─────────────────────────────────────┘
```

## 7. Performance Considerations

### 7.1 Loading States
- Skeleton loaders for content
- Progressive loading of video previews
- Lazy loading for example videos

### 7.2 Caching Strategy
- Next.js static generation for landing pages
- SWR for API calls with revalidation
- CDN caching for generated videos

### 7.3 Error Handling
- Network error recovery
- Graceful degradation for failed generations
- User-friendly error messages

## 8. Development Setup

### 8.1 Project Structure
```
frontend/
├── app/                    # Next.js app directory
│   ├── (marketing)/       # Marketing pages group
│   │   ├── page.tsx       # Landing page
│   │   ├── pricing/       # Pricing page
│   │   └── examples/      # Examples page
│   ├── generate/          # Generation interface
│   ├── preview/           # Video preview pages
│   └── api/               # API routes (proxy to backend)
├── components/            # Reusable components
│   ├── ui/               # Base UI components (shadcn)
│   ├── video/            # Video-related components
│   └── forms/            # Form components
├── lib/                  # Utilities and configurations
├── hooks/                # Custom React hooks
├── types/                # TypeScript type definitions
└── public/               # Static assets
```

### 8.2 Development Commands
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint

# Type check
npm run type-check
```

### 8.3 Environment Variables
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
```

## 9. Future Enhancements

### 9.1 Advanced Features
- **User Accounts:** Save generated videos, usage history
- **Templates:** Pre-made video templates for different cuisines
- **Batch Processing:** Generate multiple videos at once
- **A/B Testing:** Compare different video styles
- **Analytics:** Video performance tracking

### 9.2 Monetization Features
- **Credit System:** Pay-per-video or subscription plans
- **White-label:** Custom branding for agencies
- **API Access:** Developer API for integrations
- **Premium Styles:** Exclusive video styles for paid users

### 9.3 Technical Improvements
- **PWA Support:** Offline functionality
- **Real-time Updates:** WebSocket for live progress
- **Video Editor:** Basic editing capabilities
- **Social Integration:** Direct posting to social platforms

## 10. Deployment Strategy

### 10.1 Environments
- **Development:** Local development with hot reload
- **Staging:** Preview deployments for testing
- **Production:** Vercel deployment with CDN

### 10.2 CI/CD Pipeline
- Automated testing on PR creation
- Preview deployments for every branch
- Automatic production deployment on main branch merge
- Performance monitoring and alerts

### 10.3 Monitoring
- **Analytics:** Google Analytics, Mixpanel
- **Performance:** Web Vitals, Lighthouse CI
- **Errors:** Sentry error tracking
- **Uptime:** Uptime monitoring service