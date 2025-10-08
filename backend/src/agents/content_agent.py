from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from typing import Dict, Any
import logging
from .tools.content_tools import ContentGenerationTools

logger = logging.getLogger(__name__)

class ContentAgent:
    """
    Agno-powered agent for generating video scripts and promotional content
    """

    def __init__(self, model_provider: str = "openai", model_id: str = "gpt-4o-mini"):
        # Initialize the appropriate model
        if model_provider == "anthropic":
            model = Claude(id=model_id)
        else:
            model = OpenAIChat(id=model_id)

        # Initialize tools
        self.content_tools = ContentGenerationTools()

        # Create the Agno agent
        self.agent = Agent(
            name="Video Content Creator",
            model=model,
            tools=[self.content_tools],
            instructions=[
                "You are a video content creation specialist for restaurant promotional videos.",
                "Create engaging, persuasive scripts that make viewers want to visit the restaurant.",
                "Focus on emotional appeal, sensory language, and clear calls to action.",
                "Keep scripts concise but impactful - typically 30-60 seconds when spoken.",
                "Use the content generation tools to analyze data and optimize script elements.",
                "Tailor content style to match the restaurant's brand and target audience.",
                "Always include practical information like location or contact details.",
                "Make every word count - remove filler and focus on compelling benefits."
            ],
            markdown=True
        )

        logger.info("Content Agent initialized with Agno framework")

    async def generate_video_script(self, restaurant_data: Dict[str, Any], menu_data: Dict[str, Any], style: str = "casual") -> Dict[str, Any]:
        """
        Generate a complete video script based on restaurant and menu data

        Args:
            restaurant_data: Restaurant information and analysis
            menu_data: Menu information and featured items
            style: Video style (casual, professional, trendy, etc.)

        Returns:
            Dict containing the generated script and metadata
        """
        try:
            prompt = f"""
            Create a compelling promotional video script for this restaurant:

            **Restaurant Data:** {restaurant_data}
            **Menu Data:** {menu_data}
            **Requested Style:** {style}

            First, use the content generation tools to:
            1. Prepare the script data and analyze the restaurant information
            2. Suggest appropriate video styles based on the restaurant type
            3. Create optimization guidelines for the target duration

            Then create a complete video script with these sections:

            ## HOOK (3-5 seconds)
            An attention-grabbing opening that makes viewers want to keep watching

            ## MAIN CONTENT (35-50 seconds)
            - Highlight the restaurant's unique selling points
            - Feature 2-3 specific menu items with sensory descriptions
            - Include social proof (ratings, reviews) if strong
            - Emphasize atmosphere, quality, or value proposition

            ## CALL TO ACTION (5-10 seconds)
            Clear direction for viewers (visit, call, order) with practical information

            **Writing Guidelines:**
            - Use conversational, engaging language
            - Include sensory words that trigger appetite
            - Create urgency without being pushy
            - Match the tone to the restaurant's style and target audience
            - Keep total word count to 100-150 words (30-60 seconds when spoken)
            - Include natural pauses for visual elements

            **Script Format:**
            Provide the script with timing cues and visual suggestions:
            - [VISUAL: description] for video elements
            - [PAUSE] for natural breaks
            - **EMPHASIS** for key words/phrases

            End with a brief explanation of why this script approach works for this specific restaurant.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "script": response.content,
                "style": style,
                "script_generated": True
            }

        except Exception as e:
            logger.error(f"Script generation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "script_generated": False
            }

    async def create_social_media_content(self, restaurant_data: Dict[str, Any], target_platform: str = "instagram") -> Dict[str, Any]:
        """
        Create social media promotional content

        Args:
            restaurant_data: Restaurant information
            target_platform: Social media platform (instagram, facebook, tiktok, etc.)

        Returns:
            Dict containing social media content variations
        """
        try:
            prompt = f"""
            Create social media promotional content for this restaurant:

            **Restaurant Data:** {restaurant_data}
            **Target Platform:** {target_platform}

            Use the content generation tools to prepare promotional copy data, then create:

            ## POST CAPTIONS
            Create 3 variations:
            1. **Short & Punchy** (under 50 characters) - for stories/quick posts
            2. **Medium Engagement** (50-100 characters) - for main feed posts
            3. **Detailed Story** (100+ characters) - for community building

            ## HASHTAG SUGGESTIONS
            Provide relevant hashtags for:
            - Local discovery
            - Food type/cuisine
            - Restaurant experience
            - Call to action

            ## CALL-TO-ACTION OPTIONS
            Multiple CTA approaches:
            - Visit focused
            - Phone/reservation focused
            - Online ordering focused

            ## PLATFORM-SPECIFIC ADAPTATIONS
            Tailor content for {target_platform} best practices:
            - Optimal posting style
            - Character limits
            - Engagement strategies
            - Visual content suggestions

            Focus on creating scroll-stopping content that drives real visits and orders.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "social_content": response.content,
                "platform": target_platform,
                "content_created": True
            }

        except Exception as e:
            logger.error(f"Social media content creation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "content_created": False
            }

    async def optimize_script_for_duration(self, script_content: str, target_duration: int = 45) -> Dict[str, Any]:
        """
        Optimize script length for target video duration

        Args:
            script_content: Original script content
            target_duration: Target duration in seconds

        Returns:
            Dict containing optimized script
        """
        try:
            prompt = f"""
            Optimize this video script for a {target_duration}-second target duration:

            **Current Script:**
            {script_content}

            **Target Duration:** {target_duration} seconds

            Use the script optimization tools to get guidelines, then:

            1. **Analyze Current Length**: Estimate current speaking time
            2. **Identify Optimization Opportunities**: What can be tightened or expanded?
            3. **Create Optimized Version**: Rewrite to hit the target duration
            4. **Maintain Impact**: Ensure key messaging and emotional appeal remain strong

            **Optimization Techniques:**
            - Remove unnecessary words and filler
            - Combine related concepts
            - Use more powerful, concise language
            - Ensure smooth flow and natural speaking rhythm
            - Keep the most compelling elements

            Provide both the optimized script and a brief explanation of the changes made.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "optimized_script": response.content,
                "target_duration": target_duration,
                "optimization_completed": True
            }

        except Exception as e:
            logger.error(f"Script optimization failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "optimization_completed": False
            }