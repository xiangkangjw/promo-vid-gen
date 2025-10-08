from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from typing import Dict, Any, Optional
import os
import logging
from .tools.restaurant_tools import RestaurantDataTools

logger = logging.getLogger(__name__)

class RestaurantAgent:
    """
    Agno-powered agent for extracting and analyzing restaurant information
    """

    def __init__(self, model_provider: str = "openai", model_id: str = "gpt-4o-mini"):
        # Initialize the appropriate model
        if model_provider == "anthropic":
            model = Claude(id=model_id)
        else:
            model = OpenAIChat(id=model_id)

        # Initialize tools
        self.restaurant_tools = RestaurantDataTools(
            google_places_api_key=os.getenv("GOOGLE_PLACES_API_KEY")
        )

        # Create the Agno agent
        self.agent = Agent(
            name="Restaurant Data Specialist",
            model=model,
            tools=[self.restaurant_tools],
            instructions=[
                "You are a restaurant data extraction specialist.",
                "Extract comprehensive restaurant information from Google Maps URLs.",
                "Always use the restaurant tools to get accurate, up-to-date information.",
                "Provide detailed analysis of the restaurant's key characteristics.",
                "Focus on information that would be valuable for promotional video creation.",
                "If extraction fails, provide helpful suggestions for alternative approaches."
            ],
            markdown=True
        )

        logger.info("Restaurant Agent initialized with Agno framework")

    async def extract_restaurant_data(self, google_maps_url: str) -> Dict[str, Any]:
        """
        Extract restaurant data from Google Maps URL

        Args:
            google_maps_url: The Google Maps URL for the restaurant

        Returns:
            Dict containing restaurant information and analysis
        """
        try:
            prompt = f"""
            Please extract comprehensive restaurant information from this Google Maps URL: {google_maps_url}

            Use the restaurant tools to:
            1. Extract basic restaurant information (name, address, phone, website, etc.)
            2. Get ratings and review data
            3. Analyze the restaurant type and characteristics

            After extracting the data, provide a brief analysis including:
            - Key selling points for promotional content
            - Restaurant category and style
            - Notable features (high ratings, unique cuisine, etc.)
            - Recommendations for video content focus

            Format your response as structured data that can be easily used by other agents.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "agent_response": response.content,
                "data_extracted": True
            }

        except Exception as e:
            logger.error(f"Restaurant data extraction failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "data_extracted": False
            }

    async def analyze_restaurant_characteristics(self, restaurant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze restaurant characteristics for video content planning

        Args:
            restaurant_data: Previously extracted restaurant data

        Returns:
            Dict containing analysis and recommendations
        """
        try:
            prompt = f"""
            Based on this restaurant data: {restaurant_data}

            Provide a comprehensive analysis for video content creation:

            1. **Target Audience**: Who is the likely customer base?
            2. **Video Style Recommendations**: What video style would work best?
            3. **Key Messaging Points**: What should the video emphasize?
            4. **Unique Selling Propositions**: What makes this restaurant special?
            5. **Content Focus Areas**: Food, atmosphere, service, location, etc.

            Consider factors like:
            - Price range and restaurant type
            - Customer reviews and ratings
            - Location and accessibility
            - Restaurant category (casual, fine dining, fast food, etc.)

            Provide actionable recommendations for the video creation process.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "analysis": response.content,
                "recommendations_provided": True
            }

        except Exception as e:
            logger.error(f"Restaurant analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations_provided": False
            }