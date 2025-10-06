# Technical Design Document — AI Promo Creator

## 1. High-Level Architecture

```
Client (Web UI)
        ↓
FastAPI Server (Agno Framework)
        ↓
    Workflow:
┌─────────────────────────────────────────────┐
│ MapParserAgent → MenuExtractorAgent →       │
│ ScriptGeneratorAgent → VideoGeneratorAgent  │
└─────────────────────────────────────────────┘
        ↓
Storage (S3 / DynamoDB)
        ↓
User Output (MP4 + metadata)
```

## 2. Agents and Responsibilities

| Agent | Purpose | Tools / APIs | Output |
|-------|---------|--------------|--------|
| MapParserAgent | Extracts restaurant name, address, website, and optionally reviews from Google Maps URL | Google Places API / Scraper tool | JSON with structured data |
| MenuExtractorAgent | Crawls website or PDF to extract menu items | HTTP client, HTML parser, OCR (if PDF) | Menu JSON (categories, items, prices) |
| ScriptGeneratorAgent | Creates promo script & scene plan | OpenAI GPT-4 / Claude | Script text + storyboard JSON |
| VideoGeneratorAgent | Generates visuals, voiceover, and assembles final video | Pexels API (images), ElevenLabs (TTS), ffmpeg / Runway | MP4 file |
| ControllerAgent | Orchestrates workflow between all agents | Agno Workflow class | Final deliverable metadata |

## 3. Data Flow Example

**Input:**
```json
{
  "google_maps_url": "https://maps.app.goo.gl/abc123"
}
```

**↓ MapParserAgent**
```json
{
  "restaurant_name": "Oro Restaurant",
  "website": "https://www.ororestaurant.ca"
}
```

**↓ MenuExtractorAgent**
```json
{
  "menu": [
    {"category": "Starters", "items": ["Burrata", "Crab Cakes"]},
    {"category": "Mains", "items": ["Lamb Shank", "Seared Tuna"]}
  ]
}
```

**↓ ScriptGeneratorAgent**
```json
{
  "script": "Experience the taste of Italy at Oro...",
  "scenes": [
    {"text": "Welcome to Oro Restaurant", "image_prompt": "Italian dining interior"},
    {"text": "Handcrafted pastas and premium wines", "image_prompt": "close-up pasta dish"}
  ]
}
```

**↓ VideoGeneratorAgent**
→ generates visuals + TTS + ffmpeg merge
↓
**Output:** promo_video.mp4

## 4. APIs & Tools

| Function | Service / Library | Notes |
|----------|-------------------|-------|
| Map data | Google Places API | Requires API key |
| Web scraping | Playwright / Requests + BeautifulSoup | Backup for no API data |
| OCR (PDF menus) | Tesseract / Cloud Vision | Optional fallback |
| Script generation | OpenAI GPT-4 or Claude | Prompt tuned for marketing |
| Voiceover | ElevenLabs / OpenAI TTS | Multi-style voices |
| Stock footage | Pexels / Pixabay API | License-friendly |
| Video composition | ffmpeg via Agno Tool | Merge images, audio, text overlays |
| File hosting | AWS S3 / Cloudflare R2 | Store outputs |
| DB | DynamoDB | Track tasks, metadata, and usage |

## 5. Example Agno Workflow Definition

```python
from agno import Agent, Workflow

class MapParserAgent(Agent):
    def run(self, url):
        # Extract restaurant info
        return fetch_restaurant_data(url)

class MenuExtractorAgent(Agent):
    def run(self, website):
        return extract_menu_items(website)

class ScriptGeneratorAgent(Agent):
    def run(self, restaurant_info, menu):
        return generate_script(restaurant_info, menu)

class VideoGeneratorAgent(Agent):
    def run(self, script):
        return assemble_video(script)

workflow = Workflow([
    MapParserAgent(),
    MenuExtractorAgent(),
    ScriptGeneratorAgent(),
    VideoGeneratorAgent()
])
```

## 6. Deployment

- **Backend:** FastAPI (Agno Server)
- **Frontend:** Next.js (upload form + video preview)
- **Infra:** AWS Lambda or EC2 (compute), S3 (storage)
- **Monitoring:** Agno Control Plane + OpenTelemetry

## 7. Future Enhancements

- ✨ Support for TikTok-style vertical format
- 🧠 Add AI brand tone customization (e.g., luxury, street food, family-friendly)
- 💬 Add voiceover language selection
- 📈 Analytics dashboard (views, engagement metrics)