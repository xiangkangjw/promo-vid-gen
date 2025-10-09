from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from typing import Dict, Any
import logging
from .tools.menu_tools import MenuExtractionTools

logger = logging.getLogger(__name__)

class MenuAgent:
    """
    Agno-powered agent for extracting restaurant menu information
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
            name="Menu Extraction Specialist",
            model=model,
            tools=[self.menu_tools],
            instructions=[
                "You are a menu extraction specialist.",
                "Extract menu information from restaurant websites with high accuracy.",
                "Focus on getting complete menu data: item names, prices, descriptions, and categories.",
                "Return clean, structured menu data without analysis or recommendations.",
                "Ensure all menu items are properly categorized and formatted.",
                "If extraction fails, report the specific issue clearly."
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
            Dict containing clean menu data
        """
        try:
            if not website_url or website_url.strip() == "":
                return {
                    "status": "skipped",
                    "message": "No website URL provided",
                    "menu_extracted": False,
                    "menu_data": None
                }

            prompt = f"""
            Extract menu information from this restaurant website: {website_url}

            Use the menu extraction tools to get:
            1. Complete list of menu items with names, prices, and descriptions
            2. Menu categories and organization
            3. Any dietary information or special notations

            Return the extracted menu data in a clean, structured format.
            Do not provide analysis, recommendations, or suggestions - just the raw menu data.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "menu_data": response.content,
                "menu_extracted": True
            }

        except Exception as e:
            logger.error(f"Menu extraction failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "menu_extracted": False,
                "menu_data": None
            }

