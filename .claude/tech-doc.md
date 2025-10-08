# Technical Design Document — AI Promo Creator

## 1. High-Level Architecture (Agno AgentOS)

```
Client (Web UI)
        ↓
AgentOS (Agno Framework) — Production Runtime & Control Plane
        ↓
┌─────────────────────────────────────────────────────────────┐
│ Main Orchestrator Agent                                     │
│   ├── RestaurantAgent (Restaurant Data Tools)              │
│   ├── MenuAgent (Menu Extraction Tools)                    │
│   ├── ContentAgent (Content Generation Tools)              │
│   └── VideoAgent (Video Production Tools)                  │
└─────────────────────────────────────────────────────────────┘
        ↓
Persistent Storage (SQLite DB + S3 Assets)
        ↓
User Output (Complete Video Package + Analytics)
```

## 2. AgentOS Architecture Benefits

**AgentOS Features:**
- **Production Runtime**: Enterprise-grade agent hosting and management
- **Database Integration**: Built-in SQLite with conversation persistence
- **Real-time Streaming**: WebSocket support for live progress updates
- **Session Management**: Automatic user session and context handling
- **API Generation**: Automatic REST API + WebSocket endpoints
- **Authentication**: Built-in auth and security features

## 3. Specialized Agents and Toolkits

| Agent | Toolkit | Purpose | Capabilities |
|-------|---------|---------|--------------|
| **Main Orchestrator** | All Tools | Complete workflow coordination | Full video generation pipeline, progress tracking |
| **Restaurant Specialist** | RestaurantDataTools | Google Maps data extraction | Places API integration, business analysis, recommendations |
| **Menu Analyst** | MenuExtractionTools | Website menu scraping & analysis | HTTP + Playwright scraping, menu categorization, featured items |
| **Content Creator** | ContentGenerationTools | Script & promotional content | Video scripts, social media content, style optimization |
| **Video Producer** | VideoProductionTools | Production planning & assets | Stock footage search, voiceover prep, technical specs |

## 4. Toolkit Implementations

### RestaurantDataTools
- `extract_restaurant_from_maps_url()` — Google Maps URL processing
- `search_restaurant_by_name()` — Restaurant search and discovery
- `get_restaurant_details()` — Detailed business information

### MenuExtractionTools
- `extract_menu_from_website()` — Website scraping with fallbacks
- `scrape_menu_with_playwright()` — Dynamic content extraction
- `analyze_menu_structure()` — Menu categorization and analysis

### ContentGenerationTools
- `generate_video_script()` — AI-powered script creation
- `create_promotional_copy()` — Social media content generation
- `optimize_script_length()` — Duration and pacing optimization

### VideoProductionTools
- `search_stock_footage()` — Pexels API integration for assets
- `generate_voiceover()` — ElevenLabs voice synthesis preparation
- `create_video_outline()` — Complete production planning

## 5. AgentOS Data Flow

**Input to Main Orchestrator:**
```json
{
  "google_maps_url": "https://maps.app.goo.gl/abc123",
  "video_style": "casual"
}
```

**Phase 1: Restaurant Analysis**
```json
{
  "restaurant_name": "Oro Restaurant",
  "address": "123 Main St, Toronto",
  "rating": 4.7,
  "website": "https://www.ororestaurant.ca",
  "analysis": {
    "target_audience": "Fine dining enthusiasts",
    "key_selling_points": ["High rating", "Italian cuisine", "Downtown location"]
  }
}
```

**Phase 2: Menu Intelligence**
```json
{
  "menu_items": [
    {"name": "Burrata", "price": "$18", "category": "Starters"},
    {"name": "Lamb Shank", "price": "$34", "category": "Mains"}
  ],
  "featured_items": ["Burrata", "Handmade Pasta", "Osso Buco"],
  "analysis": {
    "price_range": {"min": 15, "max": 45, "avg": 28},
    "popular_items": ["Signature pasta dishes"]
  }
}
```

**Phase 3: Content Creation**
```json
{
  "script": {
    "hook": "Discover authentic Italian flavors at Oro Restaurant...",
    "main_content": "From handcrafted burrata to our signature lamb shank...",
    "call_to_action": "Reserve your table today and taste the difference."
  },
  "social_content": {
    "instagram": "🍝 Authentic Italian at Oro Restaurant! Book now!",
    "facebook": "Experience fine Italian dining in the heart of Toronto..."
  }
}
```

**Phase 4: Production Planning**
```json
{
  "production_plan": {
    "footage_requirements": ["Italian restaurant interior", "pasta preparation", "plated dishes"],
    "voiceover_specs": {"style": "warm professional", "duration": "45 seconds"},
    "technical_specs": {"format": "1080p", "aspect_ratio": "16:9"}
  },
  "timeline": {"total_time": "5m 15s", "complexity": "Medium"}
}
```

**Final Output:** Complete video package + production assets

## 6. APIs & External Services

| Function | Service / Library | Implementation |
|----------|-------------------|----------------|
| Restaurant Data | Google Places API | RestaurantDataTools with fallback scraping |
| Web Scraping | Playwright + BeautifulSoup | MenuExtractionTools with dynamic content support |
| AI Models | OpenAI GPT-4o-mini / Claude | Flexible model selection per agent |
| Voiceover | ElevenLabs TTS | VideoProductionTools with voice optimization |
| Stock Assets | Pexels API | VideoProductionTools for footage and images |
| Database | SQLite (AgentOS built-in) | Conversation persistence and session management |
| File Storage | AWS S3 | Video assets and production files |

## 7. AgentOS Implementation Example

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from agno.models.openai import OpenAIChat

# Create specialized agents with toolkits
main_orchestrator = Agent(
    name="Promo Video Creator",
    model=OpenAIChat(id="gpt-4o-mini"),
    db=SqliteDb(db_file="promo_creator.db"),
    tools=[
        RestaurantDataTools(),
        MenuExtractionTools(),
        ContentGenerationTools(),
        VideoProductionTools()
    ],
    instructions=[
        "Execute complete promotional video generation workflow",
        "Provide detailed progress updates for each phase",
        "Focus on high-impact marketing content"
    ],
    add_history_to_context=True
)

# AgentOS handles all the infrastructure
agent_os = AgentOS(agents=[main_orchestrator])
app = agent_os.get_app()  # Auto-generated FastAPI app
```

## 8. Deployment Architecture

- **Backend:** AgentOS (Agno Production Runtime)
- **Frontend:** Next.js with real-time WebSocket integration
- **Database:** SQLite for conversations + S3 for assets
- **Infrastructure:** Docker containers on cloud platforms
- **Monitoring:** Built-in AgentOS analytics and logging
- **Scaling:** AgentOS handles load balancing and agent orchestration

## 7. Future Enhancements

- ✨ Support for TikTok-style vertical format
- 🧠 Add AI brand tone customization (e.g., luxury, street food, family-friendly)
- 💬 Add voiceover language selection
- 📈 Analytics dashboard (views, engagement metrics)