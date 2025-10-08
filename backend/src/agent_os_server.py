"""
AgentOS-powered server for AI Promo Creator
Replaces the standalone FastAPI implementation with Agno's integrated AgentOS
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.duckduckgo import DuckDuckGoTools
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .agents.tools.restaurant_tools import RestaurantDataTools
from .agents.tools.menu_tools import MenuExtractionTools
from .agents.tools.content_tools import ContentGenerationTools
from .agents.tools.video_tools import VideoProductionTools
from .workflows.video_generation_workflow import (
    create_video_generation_workflow,
    create_script_only_workflow,
    create_restaurant_analysis_workflow
)

logger = logging.getLogger(__name__)

# Initialize database for persistent conversations
promo_db = SqliteDb(
    db_file="promo_creator.db",
)

def create_model(model_provider: str = "openai", model_id: str = "gpt-4o-mini"):
    """Create the appropriate model based on configuration"""
    if model_provider == "anthropic":
        return Claude(id=model_id)
    else:
        return OpenAIChat(id=model_id)

# Restaurant Data Agent - Specialized in extracting restaurant information
restaurant_agent = Agent(
    name="Restaurant Specialist",
    model=create_model(),
    db=promo_db,
    tools=[
        RestaurantDataTools(google_places_api_key=os.getenv("GOOGLE_PLACES_API_KEY")),
        DuckDuckGoTools()  # For additional research if needed
    ],
    instructions=[
        "You are a restaurant data extraction specialist for promotional video creation.",
        "Extract comprehensive restaurant information from Google Maps URLs.",
        "Analyze restaurant characteristics to provide video content recommendations.",
        "Focus on key selling points, target audience, and unique features.",
        "Always use the restaurant tools first, then provide intelligent analysis.",
        "If data extraction fails, suggest alternative approaches."
    ],
    markdown=True,
    add_history_to_context=True,
    add_datetime_to_context=True
)

# Menu Analysis Agent - Specialized in menu extraction and analysis
menu_agent = Agent(
    name="Menu Analyst",
    model=create_model(),
    db=promo_db,
    tools=[
        MenuExtractionTools()
    ],
    instructions=[
        "You are a menu analysis specialist for restaurant promotional videos.",
        "Extract and analyze menu information to identify the best items to feature.",
        "Focus on visually appealing dishes, popular items, and unique offerings.",
        "Provide recommendations for which items would work best in video content.",
        "Consider dietary options and price points for target audience appeal.",
        "If menu extraction fails, suggest creative alternatives for showcasing food."
    ],
    markdown=True,
    add_history_to_context=True
)

# Content Creation Agent - Specialized in script and promotional content
content_creator_agent = Agent(
    name="Content Creator",
    model=create_model(),
    db=promo_db,
    tools=[
        ContentGenerationTools()
    ],
    instructions=[
        "You are a video content creation specialist for restaurant promotional videos.",
        "Create engaging, persuasive scripts that drive customers to visit restaurants.",
        "Use emotional appeal, sensory language, and clear calls to action.",
        "Tailor content style to match restaurant type and target audience.",
        "Keep scripts concise but impactful (30-60 seconds when spoken).",
        "Include practical information and strong value propositions.",
        "Generate social media content as additional value."
    ],
    markdown=True,
    add_history_to_context=True
)

# Video Production Agent - Specialized in production planning
video_producer_agent = Agent(
    name="Video Producer",
    model=create_model(),
    db=promo_db,
    tools=[
        VideoProductionTools(
            pexels_api_key=os.getenv("PEXELS_API_KEY"),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY")
        )
    ],
    instructions=[
        "You are a video production specialist for restaurant promotional videos.",
        "Plan comprehensive video production including footage, audio, and editing.",
        "Source appropriate stock footage and plan professional voiceover generation.",
        "Create detailed production outlines for efficient execution.",
        "Focus on visually appealing content that showcases food attractively.",
        "Provide realistic time estimates and technical specifications.",
        "Ensure production plans are both high-quality and cost-effective."
    ],
    markdown=True,
    add_history_to_context=True
)

# Main Orchestrator Agent - Coordinates the complete workflow
main_orchestrator = Agent(
    name="Promo Video Creator",
    model=create_model(),
    db=promo_db,
    tools=[
        RestaurantDataTools(google_places_api_key=os.getenv("GOOGLE_PLACES_API_KEY")),
        MenuExtractionTools(),
        ContentGenerationTools(),
        VideoProductionTools(
            pexels_api_key=os.getenv("PEXELS_API_KEY"),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY")
        )
    ],
    instructions=[
        "You are the main coordinator for AI Promo Creator - a system that generates promotional videos for restaurants.",
        "When given a Google Maps URL, execute a complete workflow:",
        "",
        "1. **Restaurant Analysis**: Extract restaurant data, ratings, and characteristics",
        "2. **Menu Analysis**: Extract and analyze menu items for video featuring",
        "3. **Script Creation**: Generate compelling video scripts based on restaurant data",
        "4. **Production Planning**: Create comprehensive video production plans",
        "",
        "Provide detailed, step-by-step progress updates.",
        "If any step fails, offer alternative approaches.",
        "Always aim for maximum impact promotional content.",
        "Focus on driving real business results for restaurant owners.",
        "",
        "For quick requests, you can also:",
        "- Generate just a script preview",
        "- Analyze restaurant data only",
        "- Create social media content",
        "",
        "Be professional, efficient, and results-oriented."
    ],
    markdown=True,
    add_history_to_context=True,
    add_datetime_to_context=True
)

# Create Agno workflows using the factory functions
video_generation_workflow = create_video_generation_workflow(
    restaurant_agent=restaurant_agent,
    menu_agent=menu_agent,
    content_creator_agent=content_creator_agent,
    video_producer_agent=video_producer_agent,
    db=promo_db
)

script_only_workflow = create_script_only_workflow(
    restaurant_agent=restaurant_agent,
    menu_agent=menu_agent,
    content_creator_agent=content_creator_agent,
    db=promo_db
)

restaurant_analysis_workflow = create_restaurant_analysis_workflow(
    restaurant_agent=restaurant_agent,
    db=promo_db
)

# Create AgentOS with all specialized agents and workflows
agent_os = AgentOS(
    agents=[
        main_orchestrator,      # Primary agent for complete workflows
        restaurant_agent,       # Specialized restaurant analysis
        menu_agent,            # Specialized menu analysis
        content_creator_agent, # Specialized content creation
        video_producer_agent   # Specialized video production
    ],
    workflows=[
        video_generation_workflow,      # Complete video generation workflow
        script_only_workflow,          # Fast script-only workflow
        restaurant_analysis_workflow   # Restaurant analysis only
    ],
    # AgentOS automatically handles:
    # - API endpoint generation
    # - WebSocket streaming
    # - Session management
    # - Database operations
    # - Error handling
    # - Authentication (if configured)
)

# Get the FastAPI app (AgentOS creates this automatically)
app = agent_os.get_app()

# Add CORS middleware for frontend integration - MUST be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://os.agno.com",  # Allow Agno cloud interface
        "https://agno.ai",      # Allow Agno domain
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Custom endpoint for health checks
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Promo Creator AgentOS",
        "agents": [agent.name for agent in agent_os.agents],
        "version": "1.0.0"
    }

# Custom endpoint for getting agent capabilities
@app.get("/capabilities")
async def get_capabilities():
    """Get information about available agents and their capabilities"""
    return {
        "agents": {
            "main_orchestrator": {
                "name": "Promo Video Creator",
                "description": "Complete promotional video generation workflow",
                "capabilities": [
                    "Full video generation from Google Maps URL",
                    "Restaurant data extraction and analysis",
                    "Menu analysis and featured item selection",
                    "Video script generation",
                    "Production planning and asset sourcing"
                ]
            },
            "restaurant_agent": {
                "name": "Restaurant Specialist",
                "description": "Restaurant data extraction and analysis",
                "capabilities": [
                    "Google Maps URL processing",
                    "Restaurant information extraction",
                    "Business analysis and recommendations"
                ]
            },
            "menu_agent": {
                "name": "Menu Analyst",
                "description": "Menu extraction and analysis",
                "capabilities": [
                    "Website menu scraping",
                    "Menu item categorization",
                    "Featured item recommendations"
                ]
            },
            "content_creator_agent": {
                "name": "Content Creator",
                "description": "Video script and promotional content generation",
                "capabilities": [
                    "Video script generation",
                    "Social media content creation",
                    "Content optimization"
                ]
            },
            "video_producer_agent": {
                "name": "Video Producer",
                "description": "Video production planning and asset management",
                "capabilities": [
                    "Production planning",
                    "Stock footage sourcing",
                    "Voiceover preparation",
                    "Technical specifications"
                ]
            }
        },
        "workflows": {
            "video-generation": {
                "id": "video-generation",
                "name": "Video Generation Workflow",
                "description": "Complete promotional video generation from Google Maps URL to production plan",
                "endpoint": "/workflows/video-generation/runs",
                "parameters": ["message", "stream", "user_id", "session_id", "dependencies"]
            },
            "script-generation": {
                "id": "script-generation",
                "name": "Script Generation Workflow",
                "description": "Fast video script generation from Google Maps URL",
                "endpoint": "/workflows/script-generation/runs",
                "parameters": ["message", "stream", "user_id", "session_id", "dependencies"]
            },
            "restaurant-analysis": {
                "id": "restaurant-analysis",
                "name": "Restaurant Analysis Workflow",
                "description": "Extract and analyze restaurant data from Google Maps URL",
                "endpoint": "/workflows/restaurant-analysis/runs",
                "parameters": ["message", "stream", "user_id", "session_id", "dependencies"]
            }
        }
    }

if __name__ == "__main__":
    # import uvicorn

    # # AgentOS handles all the FastAPI configuration
    # # Just run with uvicorn
    # uvicorn.run(
    #     "agent_os_server:app",
    #     host=os.getenv("HOST", "0.0.0.0"),
    #     port=int(os.getenv("PORT", 8000)),
    #     reload=True if os.getenv("DEBUG", "false").lower() == "true" else False
    # )
    agent_os.serve(app= "agent_os_server:app", port=8000, reload=True)