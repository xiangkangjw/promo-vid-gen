# AI Promo Creator 

## Rules

- before you do any work, MUST view files in .claude/tasks/context_session_x.md file to get the full context (x being the id of the session we are operating in, if file doesn't exist, then create one)
- context_session_x.md should contain most of the context of what we did, overall plan, and sub agents will continuously add context to the file
- after you finish the work, MUST update/append the .claude/tasks/context_session_x.md to make sure others can get full context of what you did. you MUST preserve the existing conversation.

### Sub agents

You have access to 4 sub agents:

- product-manager: any tasks related to product questions and user behavior, consult this agent
- senior-software-engineer: any tasks related to non-trivial UI changes, consult this agent for UI engineering expertise
- senior-ux-designer: any tasks related to comply with design principles, the user experiences, consult this agent
- shadcn-architect: all tasks related to UI building and tweaking, consult this agent

Sub-agents will do research about the implementation, but you will do the actual implementation; when passing tasks to sub agent, make sure you pass the the context file, e.g. '.claude/tasks/session_context_x.md'.
After each sub agent finish the work, make sure you read the related documentation they created to get full context of the plan before you start executing.

## Project Overview
AI Promo Creator automatically generates short promotional videos for restaurants from a single Google Maps URL. The system extracts restaurant data, generates scripts, creates voiceovers, and assembles final videos.

## Architecture
- **Backend:** AgentOS (Agno Framework) - Production Runtime & Control Plane
- **Frontend:** Next.js web application with real-time WebSocket integration
- **Agents:** Restaurant Specialist, Menu Analyst, Content Creator, Video Producer, Main Orchestrator
- **Storage:** SQLite (conversations) + S3 (assets)
- **APIs:** Google Places, OpenAI/Claude, ElevenLabs, Pexels

## Project Structure
```
promo-vid-gen/
├── .claude/                 # Project documentation
│   ├── prod-doc.md         # Product requirements & user stories
│   ├── tech-doc.md         # Technical architecture & design
│   └── frontend-doc.md     # Frontend design & UI specifications
├── backend/                 # AgentOS Backend
│   ├── src/
│   │   ├── agent_os_server.py      # AgentOS server with all agents
│   │   ├── agents/                 # Agno-powered AI agents
│   │   │   ├── restaurant_agent.py # Restaurant data extraction & analysis
│   │   │   ├── menu_agent.py       # Menu extraction & featured items
│   │   │   ├── content_agent.py    # Script & promotional content generation
│   │   │   ├── video_agent.py      # Video production planning
│   │   │   └── tools/              # Specialized toolkits
│   │   │       ├── restaurant_tools.py  # Google Maps & Places integration
│   │   │       ├── menu_tools.py        # Website scraping & analysis
│   │   │       ├── content_tools.py     # Content generation utilities
│   │   │       └── video_tools.py       # Production & asset management
│   │   └── workflows/              # Workflow orchestration (legacy)
│   │       └── agno_video_workflow.py   # Complete generation pipeline
│   ├── requirements.txt    # Python dependencies (installed)
│   ├── venv/              # Python virtual environment (configured)
│   └── .env.example       # Backend environment variables
├── frontend/               # Next.js 14 React frontend (COMPLETED)
│   ├── app/               # Next.js app directory
│   │   ├── globals.css    # Global styles with Tailwind
│   │   ├── layout.tsx     # Root layout with providers
│   │   ├── page.tsx       # Landing page
│   │   ├── generate/      # Video generation interface
│   │   ├── preview/[taskId]/ # Dynamic video preview
│   │   ├── pricing/       # Pricing tiers page
│   │   └── examples/      # Video examples gallery
│   ├── components/        # React components
│   │   ├── ui/           # Base UI components (shadcn/ui)
│   │   ├── video-generator.tsx    # Main generation form
│   │   ├── progress-tracker.tsx   # Real-time progress
│   │   ├── video-player.tsx       # Video player & download
│   │   ├── error-boundary.tsx     # Global error handling
│   │   └── providers.tsx          # React Query provider
│   ├── hooks/             # Custom React hooks
│   │   └── use-video-generation.ts # Video workflow hooks
│   ├── lib/              # Utilities and configurations
│   │   ├── utils.ts      # Utility functions
│   │   ├── api-client.ts # Backend API client
│   │   ├── query-client.ts # React Query configuration
│   │   └── store.ts      # Zustand state management
│   ├── types/            # TypeScript definitions
│   │   └── index.ts      # Complete API type definitions
│   ├── package.json      # Node.js dependencies
│   ├── tsconfig.json     # TypeScript configuration
│   ├── tailwind.config.js # Tailwind CSS configuration
│   └── .env.example      # Frontend environment variables
├── tests/                 # Unit and integration tests
└── CLAUDE.md             # Project context for Claude

## Development Commands

### Backend (AgentOS)
```bash
cd backend
source venv/bin/activate           # Activate virtual environment
pip install -r requirements.txt   # Install dependencies including Agno
python -m uvicorn src.agent_os_server:app --reload  # Start AgentOS on :8000
```

### Frontend (Next.js)
```bash
cd frontend
npm install                        # Install dependencies
npm run dev                       # Start dev server on :3000
npm run build                     # Build for production
npm run type-check               # TypeScript type checking
```

### Full Stack Development
```bash
# Terminal 1 - Backend (AgentOS)
cd backend && source venv/bin/activate && python -m uvicorn src.agent_os_server:app --reload

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

### Testing
```bash
# Backend tests
cd backend && source venv/bin/activate && pytest

# Frontend tests
cd frontend && npm run test
```

## Environment Variables

### Backend (.env)
```bash
# Google APIs
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here

# AI Services  
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Voice & Media
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here

# AWS Services
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=promo-videos-bucket

# App Settings
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
```

## Implementation Status

### ✅ Completed
- **Project Structure:** Organized backend/frontend separation
- **Backend Framework:** AgentOS (Agno Framework) with production runtime
- **Agent Architecture:** Complete Agno-powered agents with specialized toolkits
- **Workflow System:** AgentOS-native workflow with real-time capabilities
- **Frontend Application:** Complete Next.js 14 implementation with all features
- **UI Components:** Full component library with video generation workflow
- **State Management:** React Query v5 + Zustand for comprehensive state handling
- **Type Safety:** Complete TypeScript definitions with strict mode
- **API Client:** Robust client with error handling and retry logic
- **Error Handling:** Global error boundaries and user-friendly error states
- **Form Validation:** React Hook Form + Zod with real-time validation
- **Progress Tracking:** Real-time polling with status updates
- **Video Player:** Custom player with download and sharing capabilities
- **Responsive Design:** Mobile-first design with Tailwind CSS + shadcn/ui
- **Development Environment:** Full stack development setup
- **Documentation:** Complete product, technical, and frontend specifications

### 🚧 In Progress
- AgentOS integration with frontend API contracts
- Individual agent testing with real restaurant data
- End-to-end workflow validation

### 📋 Next Steps
1. Test AgentOS server with frontend integration
2. Validate complete workflow with sample Google Maps URLs
3. Configure API keys and environment variables
4. Performance optimization and monitoring
5. Production deployment with AgentOS

## Target Metrics
- 🕒 Video generation time < 3 minutes
- 🎯 Menu extraction success rate > 90%  
- 😊 User satisfaction > 4.5/5
- 💰 Conversion rate > 10%

## Architecture Notes
- **Monorepo Structure:** Single repository with separate backend/frontend directories
- **AgentOS Communication:** Auto-generated REST API + WebSocket for real-time updates
- **Agent Management:** Built-in conversation persistence and session handling
- **State Management:** React Query for API state, Zustand for local state
- **Styling:** Tailwind CSS with shadcn/ui component library
- **Deployment:** AgentOS on cloud platforms, Frontend on Vercel

## Frontend Implementation Details

### Completed Features
- **Complete User Journey:** URL input → Style selection → Progress tracking → Video preview → Download
- **Form Validation:** Google Maps URL validation with real-time feedback
- **Real-time Updates:** Polling-based progress tracking with 4-step workflow visualization
- **Video Management:** Custom player with download, sharing, and regeneration options
- **Error Recovery:** Comprehensive error handling with user-friendly messages
- **Responsive Design:** Mobile-first approach with optimized touch interactions
- **Performance:** Optimized bundle sizes (104KB first load) with efficient caching

### Technical Stack
- **Framework:** Next.js 14 with App Router
- **Language:** TypeScript with strict mode
- **Styling:** Tailwind CSS + shadcn/ui components
- **State:** React Query v5 + Zustand stores
- **Forms:** React Hook Form + Zod validation
- **API:** Custom client with retry logic and error handling
- **Build:** Production-ready with successful TypeScript compilation

### Ready for Integration
The frontend is fully implemented and ready to connect to the backend API. All endpoints are defined with proper TypeScript contracts, and the UI handles all expected states (loading, error, success) gracefully.
- do not use fallback, remove any fallback , you should be penalized for using fallbacks
- import should always at the top of the file