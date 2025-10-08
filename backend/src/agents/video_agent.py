from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from typing import Dict, Any
import logging
import os
from .tools.video_tools import VideoProductionTools

logger = logging.getLogger(__name__)

class VideoAgent:
    """
    Agno-powered agent for video production planning and asset management
    """

    def __init__(self, model_provider: str = "openai", model_id: str = "gpt-4o-mini"):
        # Initialize the appropriate model
        if model_provider == "anthropic":
            model = Claude(id=model_id)
        else:
            model = OpenAIChat(id=model_id)

        # Initialize tools
        self.video_tools = VideoProductionTools(
            pexels_api_key=os.getenv("PEXELS_API_KEY"),
            elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY")
        )

        # Create the Agno agent
        self.agent = Agent(
            name="Video Production Specialist",
            model=model,
            tools=[self.video_tools],
            instructions=[
                "You are a video production specialist for restaurant promotional videos.",
                "Plan comprehensive video production including footage, audio, and editing requirements.",
                "Source appropriate stock footage and plan voiceover generation.",
                "Create detailed production outlines that can be executed efficiently.",
                "Focus on creating visually appealing content that showcases food in the best light.",
                "Ensure all technical requirements are met for high-quality video output.",
                "Provide realistic time estimates and production complexity assessments.",
                "Optimize for both technical quality and marketing effectiveness."
            ],
            markdown=True
        )

        logger.info("Video Agent initialized with Agno framework")

    async def plan_video_production(self, script_data: Dict[str, Any], restaurant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comprehensive video production plan

        Args:
            script_data: Video script and content information
            restaurant_data: Restaurant information for context

        Returns:
            Dict containing complete production plan
        """
        try:
            # Extract key terms for footage search
            restaurant_name = restaurant_data.get("restaurant_name", "restaurant")
            cuisine_type = self._extract_cuisine_type(restaurant_data)
            search_terms = [restaurant_name, cuisine_type, "food", "restaurant", "dining"]

            prompt = f"""
            Create a comprehensive video production plan for this restaurant promotional video:

            **Script Data:** {script_data}
            **Restaurant Data:** {restaurant_data}

            Use the video production tools to:
            1. Search for relevant stock footage using terms: {search_terms}
            2. Create a detailed video production outline
            3. Estimate production time and complexity

            Then provide a complete production plan including:

            ## VISUAL PLANNING
            - **Required Shots**: List all visual elements needed
            - **Footage Sources**: Stock footage vs. custom shots needed
            - **Visual Style**: Color scheme, mood, pacing
            - **Shot Sequence**: How visuals should flow with the script

            ## AUDIO PLANNING
            - **Voiceover Requirements**: Style, pace, tone specifications
            - **Background Music**: Genre and mood recommendations
            - **Sound Effects**: Ambient sounds or emphasis effects

            ## TECHNICAL SPECIFICATIONS
            - **Video Format**: Resolution, aspect ratio, frame rate
            - **Duration**: Total video length and section timing
            - **Text Overlays**: Restaurant name, contact info, CTAs
            - **Branding Elements**: Logo placement, color scheme

            ## PRODUCTION TIMELINE
            - **Phase Breakdown**: Each production step with time estimates
            - **Critical Path**: Which elements must be completed first
            - **Quality Checkpoints**: What to review at each stage

            ## DELIVERABLES
            - **Main Video**: Primary promotional video
            - **Variations**: Different aspect ratios/lengths if needed
            - **Assets**: All source files and components

            Focus on creating a production plan that delivers maximum impact while being efficient to execute.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "production_plan": response.content,
                "plan_created": True
            }

        except Exception as e:
            logger.error(f"Video production planning failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "plan_created": False
            }

    async def prepare_voiceover_generation(self, script_text: str, voice_style: str = "professional") -> Dict[str, Any]:
        """
        Prepare voiceover generation with optimized settings

        Args:
            script_text: The script text for voiceover
            voice_style: Voice style preference

        Returns:
            Dict containing voiceover preparation details
        """
        try:
            # Map voice styles to ElevenLabs settings
            voice_settings = self._get_voice_settings(voice_style)

            prompt = f"""
            Prepare voiceover generation for this script:

            **Script Text:** {script_text}
            **Voice Style:** {voice_style}

            Use the video production tools to:
            1. Generate voiceover request with appropriate settings
            2. Provide optimization recommendations

            Then analyze and recommend:

            ## VOICE CHARACTERISTICS
            - **Tone**: How the voice should sound (warm, professional, energetic, etc.)
            - **Pace**: Speaking speed and rhythm
            - **Emphasis**: Which words/phrases need special emphasis
            - **Pauses**: Where natural breaks should occur

            ## TECHNICAL SETTINGS
            - **Voice Selection**: Most appropriate voice type
            - **Audio Quality**: Settings for clear, professional output
            - **Processing**: Any post-processing needs

            ## SCRIPT OPTIMIZATION FOR VOICE
            - **Pronunciation Notes**: Difficult words or names
            - **Breathing Points**: Natural pause locations
            - **Emotional Cues**: Where tone should change
            - **Timing Adjustments**: Pacing for visual synchronization

            Ensure the voiceover will sound natural, engaging, and perfectly timed for the video content.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "voiceover_plan": response.content,
                "voice_style": voice_style,
                "voiceover_prepared": True
            }

        except Exception as e:
            logger.error(f"Voiceover preparation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "voiceover_prepared": False
            }

    async def generate_production_summary(self, production_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a final production summary with all requirements

        Args:
            production_data: All collected production planning data

        Returns:
            Dict containing comprehensive production summary
        """
        try:
            prompt = f"""
            Create a comprehensive production summary based on all planning data:

            **Production Data:** {production_data}

            Generate a final summary that includes:

            ## EXECUTIVE SUMMARY
            - **Project Overview**: One-paragraph description of the video
            - **Key Objectives**: What the video aims to achieve
            - **Target Specifications**: Duration, format, quality level

            ## PRODUCTION REQUIREMENTS
            - **Visual Assets**: Complete list of footage and images needed
            - **Audio Assets**: Voiceover, music, and sound effect requirements
            - **Technical Specs**: All technical requirements and settings

            ## PRODUCTION CHECKLIST
            A step-by-step checklist for executing the production:
            1. Pre-production tasks
            2. Asset gathering and preparation
            3. Audio production steps
            4. Video editing and assembly
            5. Review and refinement
            6. Final export and delivery

            ## QUALITY STANDARDS
            - **Visual Quality**: Standards for footage and editing
            - **Audio Quality**: Standards for voiceover and music
            - **Brand Compliance**: How to maintain restaurant branding

            ## SUCCESS METRICS
            - **Technical Metrics**: Quality benchmarks to hit
            - **Marketing Metrics**: How to measure video effectiveness

            Create a summary that serves as a complete blueprint for video production.
            """

            response = await self.agent.arun(prompt)

            return {
                "status": "success",
                "production_summary": response.content,
                "summary_generated": True
            }

        except Exception as e:
            logger.error(f"Production summary generation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "summary_generated": False
            }

    def _extract_cuisine_type(self, restaurant_data: Dict[str, Any]) -> str:
        """Extract cuisine type from restaurant data"""
        types = restaurant_data.get("restaurant_types", [])

        # Common cuisine type mapping
        cuisine_keywords = {
            "italian": "italian",
            "pizza": "pizza",
            "chinese": "chinese",
            "mexican": "mexican",
            "indian": "indian",
            "japanese": "japanese",
            "thai": "thai",
            "american": "american",
            "burger": "burger",
            "seafood": "seafood",
            "steakhouse": "steak",
            "bakery": "bakery",
            "cafe": "coffee"
        }

        for restaurant_type in types:
            for keyword, cuisine in cuisine_keywords.items():
                if keyword in restaurant_type.lower():
                    return cuisine

        return "restaurant"  # Default fallback

    def _get_voice_settings(self, voice_style: str) -> Dict[str, Any]:
        """Get voice settings based on style preference"""
        style_settings = {
            "professional": {
                "stability": 0.7,
                "similarity_boost": 0.8,
                "style": 0.2,
                "use_speaker_boost": True
            },
            "casual": {
                "stability": 0.5,
                "similarity_boost": 0.7,
                "style": 0.4,
                "use_speaker_boost": True
            },
            "energetic": {
                "stability": 0.4,
                "similarity_boost": 0.6,
                "style": 0.7,
                "use_speaker_boost": True
            },
            "warm": {
                "stability": 0.6,
                "similarity_boost": 0.8,
                "style": 0.3,
                "use_speaker_boost": True
            }
        }

        return style_settings.get(voice_style, style_settings["professional"])