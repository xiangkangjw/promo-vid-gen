from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from typing import Dict, Any
import logging
from .tools.menu_tools import MenuExtractionTools

logger = logging.getLogger(__name__)

class MenuAgent:
    """
    Agno-powered agent for extracting and analyzing restaurant menu information
    """

    def __init__(self, model_provider: str = "openai", model_id: str = "gpt-4o-mini"):
        # Initialize the appropriate model
        if model_provider == "anthropic":
            model = Claude(id=model_id)
        else:
            model = OpenAIChat(id=model_id)

        # Initialize tools
        self.menu_tools = MenuExtractionTools()

        # Create the Agno agent
        self.agent = Agent(
            name="Menu Analysis Specialist",
            model=model,
            tools=[self.menu_tools],
            instructions=[
                "You are a menu analysis specialist for restaurant promotional videos.",
                "Extract and analyze menu information to identify the best items to feature.",
                "Focus on popular items, unique dishes, and price points that appeal to customers.",
                "Identify dietary options and special categories that could attract specific audiences.",
                "Provide recommendations for which menu items would look best in video content.",
                "If menu extraction fails, provide alternative strategies for showcasing the restaurant."
            ],
            markdown=True
        )

        logger.info("Menu Agent initialized with Agno framework")

    async def extract_menu_data(self, website_url: str) -> Dict[str, Any]:
        """
        Extract menu data from restaurant website

        Args:
            website_url: The restaurant's website URL

        Returns:
            Dict containing menu information and analysis
        """
        try:
            if not website_url or website_url.strip() == "":
                return {
                    "status": "skipped",
                    "message": "No website URL provided - will focus on restaurant information instead",
                    "menu_extracted": False
                }

            prompt = f"""
            Please extract and analyze the menu from this restaurant website: {website_url}

            Use the menu extraction tools to:
            1. Extract menu items with names, prices, and descriptions
            2. Analyze the menu structure and categorize items
            3. Identify popular or signature dishes
            4. Analyze price ranges and dietary options

            After extracting the menu data, provide analysis including:
            - **Featured Items**: Which 3-5 menu items would be most appealing in a video?
            - **Price Appeal**: How to position pricing in promotional content?
            - **Unique Offerings**: What makes this menu special or different?
            - **Target Categories**: What types of customers would be attracted to this menu?
            - **Visual Recommendations**: Which dishes would photograph/film best?

            If menu extraction fails or yields limited results, suggest alternative approaches for showcasing the restaurant's food offerings.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "agent_response": response.content,
                "menu_extracted": True
            }

        except Exception as e:
            logger.error(f"Menu extraction failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "menu_extracted": False
            }

    async def recommend_featured_items(self, menu_data: Dict[str, Any], restaurant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recommend which menu items to feature in the promotional video

        Args:
            menu_data: Previously extracted menu data
            restaurant_data: Restaurant information for context

        Returns:
            Dict containing featured item recommendations
        """
        try:
            prompt = f"""
            Based on this menu data: {menu_data}
            And restaurant information: {restaurant_data}

            Recommend the best menu items to feature in a promotional video:

            1. **Top 3-5 Featured Items**: Which items should be the video stars?
               - Consider visual appeal, popularity indicators, and unique selling points
               - Think about what would make viewers hungry and want to visit

            2. **Supporting Items**: Additional items to mention or show briefly

            3. **Dietary Highlights**: Vegetarian, vegan, gluten-free options worth mentioning

            4. **Price Strategy**: How to present pricing in an appealing way

            5. **Food Styling Recommendations**: How these items should be presented visually

            Consider factors like:
            - Items that photograph well and look appetizing
            - Signature dishes or restaurant specialties
            - Items that represent good value
            - Dishes that appeal to the target demographic
            - Seasonal or trending items

            Provide specific recommendations with reasoning for each choice.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "recommendations": response.content,
                "featured_items_selected": True
            }

        except Exception as e:
            logger.error(f"Featured item recommendation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "featured_items_selected": False
            }