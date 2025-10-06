# AI Promo Creator - Claude Project Context

## Project Overview
AI Promo Creator automatically generates short promotional videos for restaurants from a single Google Maps URL. The system extracts restaurant data, generates scripts, creates voiceovers, and assembles final videos.

## Architecture
- **Backend:** FastAPI with Agno Framework
- **Frontend:** Next.js web application
- **Agents:** MapParser, MenuExtractor, ScriptGenerator, VideoGenerator, Controller
- **Storage:** S3 for files, DynamoDB for metadata
- **APIs:** Google Places, OpenAI/Claude, ElevenLabs, Pexels

## Project Structure
```
promo-vid-gen/
├── .claude/                 # Project documentation
│   ├── prod-doc.md         # Product requirements & user stories
│   ├── tech-doc.md         # Technical architecture & design
│   └── frontend-doc.md     # Frontend design & UI specifications
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── agents/         # AI agent implementations
│   │   │   ├── map_parser.py       # Google Maps data extraction
│   │   │   ├── menu_extractor.py   # Website menu scraping
│   │   │   ├── script_generator.py # AI script generation
│   │   │   └── video_generator.py  # Video assembly & rendering
│   │   ├── api/            # FastAPI routes and server
│   │   │   └── main.py     # Main FastAPI application
│   │   ├── core/           # Shared utilities and base classes
│   │   │   └── base_agent.py # Base agent with logging/validation
│   │   └── workflows/      # Workflow orchestration
│   │       └── video_workflow.py # Complete generation pipeline
│   ├── requirements.txt    # Python dependencies (installed)
│   ├── venv/              # Python virtual environment (configured)
│   └── .env.example       # Backend environment variables
├── frontend/               # Next.js 14 React frontend
│   ├── app/               # Next.js app directory
│   │   ├── globals.css    # Global styles with Tailwind
│   │   ├── layout.tsx     # Root layout component
│   │   └── page.tsx       # Landing page
│   ├── components/        # React components
│   │   └── ui/           # Base UI components (shadcn/ui)
│   ├── lib/              # Utilities and configurations
│   │   └── utils.ts      # Utility functions
│   ├── types/            # TypeScript definitions
│   │   └── index.ts      # Type definitions for API data
│   ├── package.json      # Node.js dependencies
│   ├── tsconfig.json     # TypeScript configuration
│   ├── tailwind.config.js # Tailwind CSS configuration
│   └── .env.example      # Frontend environment variables
├── tests/                 # Unit and integration tests
└── CLAUDE.md             # Project context for Claude

## Development Commands

### Backend (FastAPI)
```bash
cd backend
source venv/bin/activate           # Activate virtual environment
pip install -r requirements.txt   # Install dependencies (already done)
python -m uvicorn src.api.main:app --reload  # Start dev server on :8000
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
# Terminal 1 - Backend
cd backend && source venv/bin/activate && python -m uvicorn src.api.main:app --reload

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
- **Backend Framework:** FastAPI server with CORS configuration
- **Agent Architecture:** Complete agent implementations with base class
- **Workflow System:** End-to-end video generation pipeline
- **Frontend Framework:** Next.js 14 with TypeScript and Tailwind CSS
- **Type Safety:** Complete TypeScript definitions for all data structures
- **Development Environment:** Virtual environment and dependency management
- **Documentation:** Product, technical, and frontend design documents

### 🚧 In Progress
- API integration between frontend and backend
- Individual agent testing and refinement
- UI component development

### 📋 Next Steps
1. Install frontend dependencies and test basic setup
2. Implement video generation form interface
3. Connect frontend to backend API endpoints
4. Test complete workflow with sample Google Maps URLs
5. Add error handling and progress tracking
6. Implement video preview and download functionality

## Target Metrics
- 🕒 Video generation time < 3 minutes
- 🎯 Menu extraction success rate > 90%  
- 😊 User satisfaction > 4.5/5
- 💰 Conversion rate > 10%

## Architecture Notes
- **Monorepo Structure:** Single repository with separate backend/frontend directories
- **API Communication:** RESTful API with real-time status updates
- **State Management:** React Query for API state, Zustand for local state
- **Styling:** Tailwind CSS with shadcn/ui component library
- **Deployment:** Backend on AWS/Railway, Frontend on Vercel