# AI Promo Creator - Design System Guidelines

## Overview
This document establishes comprehensive design guidelines for the AI Promo Creator application - a SaaS platform that generates promotional videos for restaurants from Google Maps URLs. The design system prioritizes professionalism, efficiency, and trust while maintaining an approachable aesthetic for restaurant owners and marketing professionals.

## Target Users
- **Primary:** Restaurant owners (ages 30-60, varying tech literacy)
- **Secondary:** Marketing professionals (ages 25-45, high tech literacy)
- **Context:** Users need quick, professional video content with minimal learning curve

---

## 1. Design System Foundation

### Color Palette

#### Primary Brand Colors
- **Primary Blue:** `hsl(217, 91%, 60%)` - #2563eb (Trustworthy, professional AI technology)
- **Primary Dark:** `hsl(217, 91%, 45%)` - #1d4ed8 (Hover states, emphasis)
- **Success Green:** `hsl(142, 76%, 36%)` - #16a34a (Video generation success, positive feedback)
- **Warning Orange:** `hsl(25, 95%, 53%)` - #f97316 (Processing states, attention needed)

#### Supporting Colors
- **Accent Purple:** `hsl(262, 83%, 58%)` - #8b5cf6 (AI features, premium elements)
- **Neutral Gray:** `hsl(210, 40%, 96%)` - #f1f5f9 (Backgrounds, subtle elements)
- **Text Primary:** `hsl(222.2, 84%, 4.9%)` - #0f172a (Main content)
- **Text Secondary:** `hsl(215.4, 16.3%, 46.9%)` - #64748b (Secondary content)

#### Semantic Color Usage
```css
:root {
  /* Enhanced primary colors for restaurant SaaS */
  --primary: 217 91% 60%; /* Professional blue */
  --primary-foreground: 210 40% 98%;
  
  /* Success states for video generation */
  --success: 142 76% 36%;
  --success-foreground: 210 40% 98%;
  
  /* Warning states for processing */
  --warning: 25 95% 53%;
  --warning-foreground: 210 40% 98%;
  
  /* Accent for AI features */
  --accent-ai: 262 83% 58%;
  --accent-ai-foreground: 210 40% 98%;
}
```

### Typography Hierarchy

#### Font Strategy
- **Primary Font:** Inter (System: -apple-system, BlinkMacSystemFont, 'Segoe UI')
- **Mono Font:** 'JetBrains Mono', 'Fira Code', monospace (for technical elements)

#### Typography Scale
```css
/* Heading Scale */
.text-h1 { font-size: 3.5rem; font-weight: 800; line-height: 1.1; } /* Hero titles */
.text-h2 { font-size: 2.5rem; font-weight: 700; line-height: 1.2; } /* Section headers */
.text-h3 { font-size: 1.875rem; font-weight: 600; line-height: 1.3; } /* Card titles */
.text-h4 { font-size: 1.25rem; font-weight: 600; line-height: 1.4; } /* Sub-headings */

/* Body Text */
.text-body-lg { font-size: 1.125rem; line-height: 1.6; } /* Hero descriptions */
.text-body { font-size: 1rem; line-height: 1.5; } /* Standard body text */
.text-body-sm { font-size: 0.875rem; line-height: 1.4; } /* Supporting text */
.text-caption { font-size: 0.75rem; line-height: 1.3; } /* Labels, metadata */
```

### Spacing System

#### Standardized Spacing Scale
```css
/* Based on 4px base unit */
--space-1: 0.25rem; /* 4px */
--space-2: 0.5rem;  /* 8px */
--space-3: 0.75rem; /* 12px */
--space-4: 1rem;    /* 16px - base unit */
--space-6: 1.5rem;  /* 24px */
--space-8: 2rem;    /* 32px */
--space-12: 3rem;   /* 48px */
--space-16: 4rem;   /* 64px */
--space-24: 6rem;   /* 96px */
```

#### Layout Principles
- **Component Padding:** 16px (space-4) minimum for touch targets
- **Section Spacing:** 48px (space-12) between major sections
- **Card Spacing:** 24px (space-6) internal padding
- **Form Element Spacing:** 16px (space-4) between fields

---

## 2. UI/UX Guidelines

### Navigation Patterns

#### Primary Navigation Structure
```
Header Navigation:
├── Logo + Brand Name (left)
├── Primary Actions (center)
│   ├── Generate Video (CTA)
│   ├── Examples
│   └── Pricing
└── Account/Auth (right)
    ├── Sign In
    └── Dashboard (authenticated)
```

#### Navigation Behavior
- **Sticky Header:** Always visible during scroll
- **Active States:** Clear visual indication of current page
- **Mobile First:** Responsive hamburger menu below 768px
- **Breadcrumbs:** For multi-step video generation process

### Form Design Standards

#### Input Field Patterns
```tsx
// Standard Input Field
<div className="space-y-2">
  <label className="text-sm font-medium text-foreground">
    Restaurant URL
  </label>
  <input 
    type="url"
    placeholder="https://maps.google.com/..."
    className="w-full h-12 px-4 border rounded-lg border-input focus:border-primary focus:ring-2 focus:ring-primary/20"
  />
  <p className="text-xs text-muted-foreground">
    Paste your Google Maps restaurant link
  </p>
</div>
```

#### Form Validation
- **Real-time Validation:** Immediate feedback on URL format
- **Error States:** Red border with descriptive error message
- **Success States:** Green border with checkmark icon
- **Loading States:** Spinner with progress indication

### Interactive States and Feedback

#### Button State System
```tsx
// Primary CTA Button
<Button className="bg-primary hover:bg-primary/90 active:bg-primary/80 disabled:bg-primary/50">
  
// Secondary Action Button  
<Button variant="outline" className="border-primary text-primary hover:bg-primary/5">

// Destructive Action
<Button variant="destructive" className="bg-destructive hover:bg-destructive/90">
```

#### Micro-interactions
- **Hover Transitions:** 150ms ease-out for smooth feel
- **Loading Animations:** Skeleton screens during content loading
- **Success Animations:** Subtle check animation for completed actions
- **Progress Indicators:** Clear visual feedback for video generation

### Responsive Design Approach

#### Breakpoint Strategy
```css
/* Mobile First Approach */
.container {
  @screen sm { max-width: 640px; }  /* Small tablets */
  @screen md { max-width: 768px; }  /* Tablets */
  @screen lg { max-width: 1024px; } /* Small laptops */
  @screen xl { max-width: 1280px; } /* Desktop */
  @screen 2xl { max-width: 1400px; } /* Large desktop */
}
```

#### Component Responsiveness
- **Grid Layouts:** 1 column mobile → 2 column tablet → 3 column desktop
- **Typography:** Responsive font scaling (clamp functions)
- **Spacing:** Reduced padding/margins on mobile devices
- **Touch Targets:** Minimum 44px height for mobile interactions

---

## 3. Brand Identity

### Visual Style Direction

#### Core Brand Attributes
- **Professional:** Conveys reliability and business-grade quality
- **Efficient:** Emphasizes speed and automation benefits
- **Accessible:** Welcoming to users with varying technical expertise
- **Trustworthy:** Builds confidence in AI-powered technology

#### Visual Language
- **Clean Minimalism:** Focused layouts with strategic white space
- **Subtle Depth:** Gentle shadows and borders for visual hierarchy
- **Technology Forward:** Modern interfaces that feel cutting-edge
- **Restaurant Friendly:** Warm accents that appeal to food industry

### Icon Usage and Illustration Style

#### Icon System (Lucide React)
```tsx
// Primary Action Icons
<MapPin className="w-5 h-5" />     // Location/URL input
<Bot className="w-5 h-5" />        // AI processing
<Video className="w-5 h-5" />      // Video generation
<Download className="w-5 h-5" />   // File download
<Clock className="w-5 h-5" />      // Time/speed
<Star className="w-5 h-5" />       // Quality/rating
<Zap className="w-5 h-5" />        // Speed/power
```

#### Illustration Guidelines
- **Style:** Simple, outlined illustrations with minimal color
- **Usage:** Hero sections, empty states, onboarding flows
- **Tone:** Professional but approachable, avoid overly technical imagery
- **Restaurant Focus:** Include food/restaurant imagery where appropriate

### Button and CTA Design Patterns

#### Primary CTA Hierarchy
```tsx
// Hero CTA - Maximum prominence
<Button size="lg" className="bg-primary text-white px-8 py-4 text-lg font-semibold">
  Start Creating Videos
  <ArrowRight className="ml-2 w-5 h-5" />
</Button>

// Secondary Action - Supporting prominence  
<Button variant="outline" size="lg" className="border-primary text-primary">
  View Examples
</Button>

// Tertiary Action - Minimal prominence
<Button variant="ghost" className="text-muted-foreground hover:text-foreground">
  Learn More
</Button>
```

---

## 4. Component Architecture

### Required shadcn/ui Components

#### Immediate Installation Needs
```bash
# Core UI Components
npx shadcn-ui@latest add input textarea select
npx shadcn-ui@latest add progress dialog sheet
npx shadcn-ui@latest add alert alert-dialog
npx shadcn-ui@latest add tabs accordion
npx shadcn-ui@latest add avatar dropdown-menu
npx shadcn-ui@latest add skeleton loading-spinner

# Form Components  
npx shadcn-ui@latest add form label
npx shadcn-ui@latest add checkbox radio-group switch

# Data Display
npx shadcn-ui@latest add table badge
npx shadcn-ui@latest add tooltip popover

# Navigation
npx shadcn-ui@latest add breadcrumb
npx shadcn-ui@latest add command
```

#### Priority Installation Order
1. **High Priority:** `input`, `progress`, `dialog`, `alert`
2. **Medium Priority:** `form`, `tabs`, `skeleton`
3. **Low Priority:** `table`, `command`, `accordion`

### Custom Component Patterns

#### Video Generation Status Component
```tsx
// Custom component for video generation workflow
export const VideoGenerationStatus = ({
  stage,
  progress,
  message
}: {
  stage: 'parsing' | 'script' | 'voice' | 'video' | 'complete'
  progress: number
  message?: string
}) => {
  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-primary" />
          Generating Your Video
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <Progress value={progress} className="w-full" />
        <div className="text-center">
          <p className="text-sm text-muted-foreground">{message}</p>
        </div>
      </CardContent>
    </Card>
  )
}
```

#### Restaurant URL Input Component
```tsx
export const RestaurantUrlInput = ({
  value,
  onChange,
  onSubmit,
  isLoading
}: {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  isLoading: boolean
}) => {
  return (
    <div className="w-full max-w-2xl space-y-4">
      <div className="flex gap-2">
        <Input
          type="url"
          placeholder="https://maps.google.com/your-restaurant"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="flex-1"
        />
        <Button 
          onClick={onSubmit}
          disabled={isLoading || !value}
          className="px-6"
        >
          {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Generate'}
        </Button>
      </div>
    </div>
  )
}
```

### Layout and Container Structures

#### Page Layout Pattern
```tsx
export const PageLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur">
        {/* Navigation content */}
      </nav>
      
      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      
      {/* Footer */}
      <footer className="border-t bg-muted/30">
        {/* Footer content */}
      </footer>
    </div>
  )
}
```

---

## 5. User Experience Flow

### Landing Page Optimization

#### Above the Fold Strategy
1. **Value Proposition:** Clear headline about video generation from Google Maps URLs
2. **Social Proof:** Statistics (3min generation, 90% success rate)
3. **Primary CTA:** "Start Creating" button prominently displayed
4. **Visual Proof:** Hero video or sample output preview

#### Trust Building Elements
- **Customer Testimonials:** Restaurant owner quotes with photos
- **Brand Logos:** Recognizable restaurant chains using the service
- **Security Badges:** Data protection and privacy certifications
- **Process Transparency:** Clear explanation of AI workflow

### Video Generation Workflow Design

#### Multi-Step Process Flow
```
Step 1: URL Input
├── URL validation
├── Restaurant detection
└── Continue to generation

Step 2: AI Processing
├── Data extraction (30%)
├── Script generation (60%)
├── Voice synthesis (80%)
└── Video assembly (100%)

Step 3: Preview & Download
├── Video preview player
├── Edit options (if needed)
└── Download & sharing options
```

#### Workflow State Management
```tsx
type VideoGenerationState = {
  stage: 'input' | 'processing' | 'preview' | 'complete'
  progress: number
  data: {
    url?: string
    restaurant?: RestaurantData
    script?: string
    videoUrl?: string
  }
  error?: string
}
```

### Progress Indicators and Status Communication

#### Progress Visualization
```tsx
const ProcessingStages = [
  { id: 'parsing', label: 'Analyzing Restaurant', icon: MapPin },
  { id: 'menu', label: 'Extracting Menu Data', icon: ChefHat },
  { id: 'script', label: 'Writing Script', icon: Edit },
  { id: 'voice', label: 'Generating Voiceover', icon: Mic },
  { id: 'video', label: 'Creating Video', icon: Video },
  { id: 'complete', label: 'Ready!', icon: CheckCircle }
]
```

#### Real-time Status Updates
- **WebSocket Connection:** Live progress updates from backend
- **Estimated Time:** Dynamic time remaining calculations
- **Error Recovery:** Clear error messages with retry options
- **Cancel Option:** Allow users to stop generation if needed

### Error Handling and Empty States

#### Error State Categories
```tsx
// Network/API Errors
<Alert variant="destructive">
  <AlertTriangle className="h-4 w-4" />
  <AlertTitle>Connection Error</AlertTitle>
  <AlertDescription>
    Unable to connect to our servers. Please check your internet connection and try again.
  </AlertDescription>
</Alert>

// Invalid URL Errors
<Alert variant="warning">
  <Info className="h-4 w-4" />
  <AlertTitle>Invalid Restaurant URL</AlertTitle>
  <AlertDescription>
    Please provide a valid Google Maps restaurant link. 
    <Button variant="link" className="p-0 h-auto">See examples</Button>
  </AlertDescription>
</Alert>

// Processing Errors
<Alert variant="destructive">
  <Bot className="h-4 w-4" />
  <AlertTitle>Generation Failed</AlertTitle>
  <AlertDescription>
    We couldn't extract enough information from this restaurant. Please try a different URL.
  </AlertDescription>
</Alert>
```

#### Empty State Design
```tsx
const EmptyState = ({ 
  icon: Icon, 
  title, 
  description, 
  action 
}: EmptyStateProps) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-4">
        <Icon className="w-8 h-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-muted-foreground mb-6 max-w-sm">{description}</p>
      {action}
    </div>
  )
}
```

---

## Implementation Priority

### Phase 1: Core Components (Week 1)
1. Install required shadcn/ui components (input, progress, dialog, alert)
2. Update color system with enhanced primary colors
3. Create RestaurantUrlInput component
4. Implement VideoGenerationStatus component

### Phase 2: Enhanced UX (Week 2)
1. Add form validation and error handling
2. Implement progress tracking system
3. Create empty states and error components
4. Add micro-interactions and animations

### Phase 3: Polish & Optimization (Week 3)
1. Fine-tune responsive behavior
2. Add accessibility improvements
3. Implement loading states and skeletons
4. Optimize performance and bundle size

---

## Notes for Implementation

### Important Considerations
1. **Accessibility:** All components must meet WCAG 2.1 AA standards
2. **Performance:** Lazy load non-critical components, optimize images
3. **SEO:** Implement proper meta tags and structured data
4. **Analytics:** Track user interactions for conversion optimization
5. **Mobile Experience:** Prioritize mobile usability for restaurant owners

### Technical Requirements
- **TypeScript:** Strict type checking for all components
- **Testing:** Unit tests for custom components
- **Documentation:** Storybook documentation for component library
- **Linting:** ESLint and Prettier for code consistency

This design system provides a comprehensive foundation for building a professional, user-friendly SaaS application that serves restaurant owners effectively while maintaining modern design standards and technical excellence.