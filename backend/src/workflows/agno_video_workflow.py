from typing import Dict, Any
import logging
import asyncio
from ..agents.restaurant_agent import RestaurantAgent
from ..agents.menu_agent import MenuAgent
from ..agents.content_agent import ContentAgent
from ..agents.video_agent import VideoAgent

logger = logging.getLogger(__name__)

class AgnoVideoWorkflow:
    """
    Complete video generation workflow using Agno agents
    """

    def __init__(self, model_provider: str = "openai", model_id: str = "gpt-4o-mini"):
        self.restaurant_agent = RestaurantAgent(model_provider, model_id)
        self.menu_agent = MenuAgent(model_provider, model_id)
        self.content_agent = ContentAgent(model_provider, model_id)
        self.video_agent = VideoAgent(model_provider, model_id)

        logger.info("Agno Video Workflow initialized")

    async def generate_promotional_video(self, google_maps_url: str, video_style: str = "casual") -> Dict[str, Any]:
        """
        Generate a complete promotional video from Google Maps URL

        Args:
            google_maps_url: Restaurant's Google Maps URL
            video_style: Video style preference (casual, professional, trendy, etc.)

        Returns:
            Dict containing complete video generation results
        """
        workflow_results = {
            "status": "in_progress",
            "phases": {
                "restaurant_data": {"completed": False},
                "menu_analysis": {"completed": False},
                "content_creation": {"completed": False},
                "video_production": {"completed": False}
            },
            "results": {}
        }

        try:
            # Phase 1: Restaurant Data Extraction
            logger.info("Phase 1: Extracting restaurant data")
            workflow_results["phases"]["restaurant_data"]["status"] = "in_progress"

            restaurant_data = await self.restaurant_agent.extract_restaurant_data(google_maps_url)

            if restaurant_data["status"] != "success":
                return self._handle_workflow_error("restaurant_data", restaurant_data, workflow_results)

            # Get restaurant analysis
            restaurant_analysis = await self.restaurant_agent.analyze_restaurant_characteristics(restaurant_data)
            restaurant_data["analysis"] = restaurant_analysis

            workflow_results["results"]["restaurant_data"] = restaurant_data
            workflow_results["phases"]["restaurant_data"]["completed"] = True
            workflow_results["phases"]["restaurant_data"]["status"] = "completed"

            # Phase 2: Menu Analysis
            logger.info("Phase 2: Analyzing menu data")
            workflow_results["phases"]["menu_analysis"]["status"] = "in_progress"

            # Extract website URL from restaurant data
            website_url = self._extract_website_url(restaurant_data)

            menu_data = await self.menu_agent.extract_menu_data(website_url)

            # Get featured items recommendations even if menu extraction had limited success
            featured_items = await self.menu_agent.recommend_featured_items(menu_data, restaurant_data)
            menu_data["featured_items"] = featured_items

            workflow_results["results"]["menu_data"] = menu_data
            workflow_results["phases"]["menu_analysis"]["completed"] = True
            workflow_results["phases"]["menu_analysis"]["status"] = "completed"

            # Phase 3: Content Creation
            logger.info("Phase 3: Creating video content")
            workflow_results["phases"]["content_creation"]["status"] = "in_progress"

            script_data = await self.content_agent.generate_video_script(
                restaurant_data, menu_data, video_style
            )

            if script_data["status"] != "success":
                return self._handle_workflow_error("content_creation", script_data, workflow_results)

            # Generate social media content as bonus
            social_content = await self.content_agent.create_social_media_content(restaurant_data)
            script_data["social_content"] = social_content

            workflow_results["results"]["content_data"] = script_data
            workflow_results["phases"]["content_creation"]["completed"] = True
            workflow_results["phases"]["content_creation"]["status"] = "completed"

            # Phase 4: Video Production Planning
            logger.info("Phase 4: Planning video production")
            workflow_results["phases"]["video_production"]["status"] = "in_progress"

            production_plan = await self.video_agent.plan_video_production(script_data, restaurant_data)

            if production_plan["status"] != "success":
                return self._handle_workflow_error("video_production", production_plan, workflow_results)

            # Prepare voiceover
            script_text = self._extract_script_text(script_data)
            voiceover_plan = await self.video_agent.prepare_voiceover_generation(script_text, video_style)
            production_plan["voiceover"] = voiceover_plan

            # Generate final production summary
            production_summary = await self.video_agent.generate_production_summary({
                "restaurant_data": restaurant_data,
                "menu_data": menu_data,
                "script_data": script_data,
                "production_plan": production_plan
            })
            production_plan["summary"] = production_summary

            workflow_results["results"]["video_production"] = production_plan
            workflow_results["phases"]["video_production"]["completed"] = True
            workflow_results["phases"]["video_production"]["status"] = "completed"

            # Complete workflow
            workflow_results["status"] = "completed"
            workflow_results["completion_time"] = self._estimate_total_time(workflow_results)

            logger.info("Video generation workflow completed successfully")
            return workflow_results

        except Exception as e:
            logger.error(f"Workflow failed: {str(e)}")
            workflow_results["status"] = "error"
            workflow_results["error"] = str(e)
            return workflow_results

    async def generate_script_only(self, google_maps_url: str, video_style: str = "casual") -> Dict[str, Any]:
        """
        Generate just the video script (faster workflow)

        Args:
            google_maps_url: Restaurant's Google Maps URL
            video_style: Video style preference

        Returns:
            Dict containing script generation results
        """
        try:
            # Get restaurant data
            restaurant_data = await self.restaurant_agent.extract_restaurant_data(google_maps_url)

            if restaurant_data["status"] != "success":
                return restaurant_data

            # Get basic menu analysis (faster)
            website_url = self._extract_website_url(restaurant_data)
            menu_data = await self.menu_agent.extract_menu_data(website_url)

            # Generate script
            script_data = await self.content_agent.generate_video_script(
                restaurant_data, menu_data, video_style
            )

            return {
                "status": "success",
                "script_data": script_data,
                "restaurant_data": restaurant_data,
                "menu_data": menu_data,
                "workflow_type": "script_only"
            }

        except Exception as e:
            logger.error(f"Script generation failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def analyze_restaurant_only(self, google_maps_url: str) -> Dict[str, Any]:
        """
        Analyze restaurant data only (for preview/validation)

        Args:
            google_maps_url: Restaurant's Google Maps URL

        Returns:
            Dict containing restaurant analysis
        """
        try:
            restaurant_data = await self.restaurant_agent.extract_restaurant_data(google_maps_url)

            if restaurant_data["status"] == "success":
                analysis = await self.restaurant_agent.analyze_restaurant_characteristics(restaurant_data)
                restaurant_data["detailed_analysis"] = analysis

            return restaurant_data

        except Exception as e:
            logger.error(f"Restaurant analysis failed: {str(e)}")
            return {"status": "error", "error": str(e)}

    def _extract_website_url(self, restaurant_data: Dict[str, Any]) -> str:
        """Extract website URL from restaurant data"""
        # Try to extract from agent response or fall back to empty string
        if "agent_response" in restaurant_data:
            # The agent response might contain structured data
            # For now, return empty string and let the menu agent handle it
            return ""
        return ""

    def _extract_script_text(self, script_data: Dict[str, Any]) -> str:
        """Extract clean script text from content data"""
        if "script" in script_data:
            script_content = script_data["script"]
            # The script is in the agent response - return as is for now
            # In a real implementation, you might want to parse and clean this
            return str(script_content)
        return "No script content available"

    def _handle_workflow_error(self, phase: str, error_data: Dict[str, Any], workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Handle errors in workflow phases"""
        workflow_results["status"] = "error"
        workflow_results["failed_phase"] = phase
        workflow_results["error"] = error_data.get("error", "Unknown error")
        workflow_results["phases"][phase]["status"] = "failed"

        logger.error(f"Workflow failed at phase {phase}: {workflow_results['error']}")
        return workflow_results

    def _estimate_total_time(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate total completion time"""
        # Base time estimates for each phase
        phase_times = {
            "restaurant_data": 45,  # seconds
            "menu_analysis": 60,
            "content_creation": 90,
            "video_production": 120
        }

        total_estimated = sum(phase_times.values())

        return {
            "total_seconds": total_estimated,
            "formatted": f"{total_estimated // 60}m {total_estimated % 60}s",
            "phase_breakdown": phase_times
        }