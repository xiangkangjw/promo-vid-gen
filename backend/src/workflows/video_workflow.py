from typing import Dict, Any
import asyncio
from src.core.base_agent import BaseAgent
from src.agents.map_parser import MapParserAgent
from src.agents.menu_extractor import MenuExtractorAgent
from src.agents.script_generator import ScriptGeneratorAgent
from src.agents.video_generator import VideoGeneratorAgent

class VideoWorkflow:
    """
    Orchestrates the complete video generation workflow
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Initialize agents
        self.map_parser = MapParserAgent(config)
        self.menu_extractor = MenuExtractorAgent(config)
        self.script_generator = ScriptGeneratorAgent(config)
        self.video_generator = VideoGeneratorAgent(config)
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete video generation workflow
        
        Args:
            input_data: {
                "google_maps_url": str,
                "style": str,  # luxury, casual, street_food
                "duration": int  # seconds
            }
            
        Returns:
            {
                "video_path": str,
                "thumbnail_path": str,
                "restaurant_info": Dict,
                "menu_data": Dict,
                "script_data": Dict,
                "video_metadata": Dict,
                "task_id": str,
                "status": "completed|failed",
                "error": str  # if failed
            }
        """
        task_id = input_data.get("task_id", "workflow")
        
        try:
            print(f"[{task_id}] Starting video generation workflow")
            
            # Step 1: Parse Google Maps URL
            print(f"[{task_id}] Step 1: Parsing Google Maps URL")
            restaurant_info = await self.map_parser.run({
                "google_maps_url": input_data["google_maps_url"]
            })
            
            # Step 2: Extract menu
            print(f"[{task_id}] Step 2: Extracting menu")
            menu_data = await self.menu_extractor.run({
                "website": restaurant_info.get("website", ""),
                "restaurant_name": restaurant_info.get("restaurant_name", "Restaurant")
            })
            
            # Step 3: Generate script
            print(f"[{task_id}] Step 3: Generating script")
            script_data = await self.script_generator.run({
                "restaurant_name": restaurant_info["restaurant_name"],
                "address": restaurant_info.get("address", ""),
                "menu": menu_data["menu"],
                "style": input_data.get("style", "casual"),
                "duration": input_data.get("duration", 30)
            })
            
            # Step 4: Generate video
            print(f"[{task_id}] Step 4: Generating video")
            video_result = await self.video_generator.run({
                "script": script_data["script"],
                "scenes": script_data["scenes"],
                "restaurant_name": restaurant_info["restaurant_name"],
                "style": script_data["style"]
            })
            
            print(f"[{task_id}] Workflow completed successfully")
            
            return {
                "video_path": video_result["video_path"],
                "thumbnail_path": video_result["thumbnail_path"],
                "restaurant_info": restaurant_info,
                "menu_data": menu_data,
                "script_data": script_data,
                "video_metadata": {
                    "duration": video_result["duration"],
                    "file_size": video_result["file_size"],
                    "resolution": video_result["resolution"]
                },
                "task_id": task_id,
                "status": "completed"
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"[{task_id}] Workflow failed: {error_msg}")
            
            return {
                "task_id": task_id,
                "status": "failed",
                "error": error_msg
            }
    
    async def run_step(self, step: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run individual workflow step for testing/debugging
        
        Args:
            step: "map_parser", "menu_extractor", "script_generator", "video_generator"
            input_data: Input data for the specific step
            
        Returns:
            Step output data
        """
        agents = {
            "map_parser": self.map_parser,
            "menu_extractor": self.menu_extractor,
            "script_generator": self.script_generator,
            "video_generator": self.video_generator
        }
        
        if step not in agents:
            raise ValueError(f"Unknown step: {step}")
        
        agent = agents[step]
        return await agent.run(input_data)
    
    def get_workflow_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get workflow status (placeholder for database integration)
        """
        # TODO: Implement database lookup
        return {
            "task_id": task_id,
            "status": "processing",
            "current_step": "script_generator",
            "progress": 75,
            "estimated_completion": "2 minutes"
        }