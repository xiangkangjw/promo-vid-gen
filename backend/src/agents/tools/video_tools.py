from typing import Dict, Any, List
from agno.tools import Toolkit
import logging
import os
import requests

logger = logging.getLogger(__name__)

class VideoProductionTools(Toolkit):
    """
    Tools for video production and asset management
    """

    def __init__(self, pexels_api_key: str = None, elevenlabs_api_key: str = None):
        self.pexels_api_key = pexels_api_key or os.getenv("PEXELS_API_KEY")
        self.elevenlabs_api_key = elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY")

        super().__init__(
            name="VideoProductionTools",
            tools=[
                self.search_stock_footage,
                self.generate_voiceover,
                self.create_video_outline,
                self.estimate_production_time
            ]
        )

    def search_stock_footage(self, search_terms: List[str], video_type: str = "food") -> Dict[str, Any]:
        """
        Search for relevant stock footage and images for the video.

        Args:
            search_terms (list): List of search terms (e.g., ["pizza", "restaurant", "cooking"])
            video_type (str): Type of video content needed

        Returns:
            Dict with suggested footage and images
        """
        try:
            if not self.pexels_api_key:
                return {"error": "Pexels API key not configured"}

            footage_suggestions = []

            for term in search_terms[:5]:  # Limit to 5 searches
                try:
                    # Search for videos
                    video_response = self._search_pexels_videos(term)
                    if video_response:
                        footage_suggestions.extend(video_response)

                    # Search for images
                    image_response = self._search_pexels_images(term)
                    if image_response:
                        footage_suggestions.extend(image_response)

                except Exception as e:
                    logger.warning(f"Search failed for term '{term}': {str(e)}")
                    continue

            return {
                "footage_suggestions": footage_suggestions[:20],  # Limit results
                "search_terms_used": search_terms,
                "total_results": len(footage_suggestions)
            }

        except Exception as e:
            logger.error(f"Error searching stock footage: {str(e)}")
            return {"error": str(e)}

    def generate_voiceover(self, script_text: str, voice_settings: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate voiceover audio from script text.

        Args:
            script_text (str): The script text to convert to speech
            voice_settings (dict): Voice configuration (voice_id, stability, etc.)

        Returns:
            Dict with voiceover generation details
        """
        try:
            if not self.elevenlabs_api_key:
                return {"error": "ElevenLabs API key not configured"}

            if not script_text.strip():
                return {"error": "No script text provided"}

            # Default voice settings
            default_settings = {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }

            settings = {**default_settings, **(voice_settings or {})}

            # Prepare voiceover request data
            voiceover_request = {
                "script_text": script_text,
                "voice_settings": settings,
                "estimated_duration": len(script_text.split()) / 2.5,  # ~2.5 words per second
                "character_count": len(script_text),
                "status": "prepared_for_generation"
            }

            return {
                "voiceover_request": voiceover_request,
                "message": "Voiceover request prepared. Use ElevenLabs API to generate audio."
            }

        except Exception as e:
            logger.error(f"Error preparing voiceover: {str(e)}")
            return {"error": str(e)}

    def create_video_outline(self, script_data: Dict[str, Any], footage_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a detailed video production outline.

        Args:
            script_data (dict): Script content and timing
            footage_data (dict): Available footage and assets

        Returns:
            Dict with complete video production outline
        """
        try:
            outline = {
                "video_structure": self._create_video_structure(),
                "timing_breakdown": self._create_timing_breakdown(script_data),
                "visual_requirements": self._analyze_visual_requirements(script_data, footage_data),
                "audio_requirements": self._analyze_audio_requirements(script_data),
                "production_notes": self._generate_production_notes()
            }

            return {
                "production_outline": outline,
                "estimated_complexity": self._estimate_complexity(outline),
                "status": "outline_ready"
            }

        except Exception as e:
            logger.error(f"Error creating video outline: {str(e)}")
            return {"error": str(e)}

    def estimate_production_time(self, video_outline: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate production time based on video complexity.

        Args:
            video_outline (dict): Video production outline

        Returns:
            Dict with time estimates for each production phase
        """
        try:
            base_times = {
                "script_processing": 30,  # seconds
                "voiceover_generation": 60,
                "footage_compilation": 120,
                "video_editing": 180,
                "final_rendering": 90
            }

            complexity_multiplier = video_outline.get("estimated_complexity", {}).get("multiplier", 1.0)

            estimated_times = {
                phase: int(time * complexity_multiplier)
                for phase, time in base_times.items()
            }

            total_time = sum(estimated_times.values())

            return {
                "phase_estimates": estimated_times,
                "total_estimated_time": total_time,
                "complexity_factor": complexity_multiplier,
                "estimated_completion": f"{total_time // 60}m {total_time % 60}s"
            }

        except Exception as e:
            logger.error(f"Error estimating production time: {str(e)}")
            return {"error": str(e)}

    def _search_pexels_videos(self, query: str) -> List[Dict[str, Any]]:
        """Search Pexels for videos"""
        try:
            headers = {"Authorization": self.pexels_api_key}
            params = {"query": query, "per_page": 5, "orientation": "landscape"}

            response = requests.get(
                "https://api.pexels.com/videos/search",
                headers=headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                videos = []

                for video in data.get("videos", []):
                    videos.append({
                        "type": "video",
                        "id": video["id"],
                        "url": video["video_files"][0]["link"] if video["video_files"] else "",
                        "thumbnail": video["image"],
                        "duration": video["duration"],
                        "tags": [query],
                        "description": f"Stock video: {query}"
                    })

                return videos

        except Exception as e:
            logger.warning(f"Pexels video search failed: {str(e)}")

        return []

    def _search_pexels_images(self, query: str) -> List[Dict[str, Any]]:
        """Search Pexels for images"""
        try:
            headers = {"Authorization": self.pexels_api_key}
            params = {"query": query, "per_page": 3, "orientation": "landscape"}

            response = requests.get(
                "https://api.pexels.com/v1/search",
                headers=headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                images = []

                for photo in data.get("photos", []):
                    images.append({
                        "type": "image",
                        "id": photo["id"],
                        "url": photo["src"]["large"],
                        "thumbnail": photo["src"]["medium"],
                        "photographer": photo["photographer"],
                        "tags": [query],
                        "description": f"Stock image: {query}"
                    })

                return images

        except Exception as e:
            logger.warning(f"Pexels image search failed: {str(e)}")

        return []

    def _create_video_structure(self) -> Dict[str, Any]:
        """Create standard video structure template"""
        return {
            "intro": {
                "duration": "3-5 seconds",
                "purpose": "Hook viewer, show restaurant name",
                "visual_style": "Eye-catching opening shot"
            },
            "main_content": {
                "duration": "35-50 seconds",
                "purpose": "Showcase food, atmosphere, unique selling points",
                "visual_style": "Mix of food shots, interior, customer experience"
            },
            "call_to_action": {
                "duration": "5-10 seconds",
                "purpose": "Drive action (visit, call, order)",
                "visual_style": "Contact info, location, clear CTA"
            }
        }

    def _create_timing_breakdown(self, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create timing breakdown based on script"""
        script_length = len(script_data.get("script_text", "").split()) if script_data.get("script_text") else 100
        estimated_duration = script_length / 2.5  # words per second

        return {
            "total_script_duration": f"{estimated_duration:.1f} seconds",
            "recommended_video_length": f"{max(30, min(60, estimated_duration + 10)):.0f} seconds",
            "pacing": "Medium-fast for engagement",
            "pauses_for_visuals": "2-3 second pauses between sections"
        }

    def _analyze_visual_requirements(self, script_data: Dict[str, Any], footage_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visual requirements based on content"""
        return {
            "required_shots": [
                "Restaurant exterior/signage",
                "Interior atmosphere",
                "Food preparation/plating",
                "Signature dishes",
                "Happy customers (if available)"
            ],
            "visual_style": "Warm, appetizing, professional",
            "color_palette": "Warm tones, food-focused",
            "available_footage": len(footage_data.get("footage_suggestions", [])),
            "additional_footage_needed": self._calculate_additional_footage_needed(footage_data)
        }

    def _analyze_audio_requirements(self, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze audio requirements"""
        return {
            "voiceover": {
                "style": "Professional, warm, engaging",
                "pacing": "Clear and moderate speed",
                "tone": "Friendly and appetizing"
            },
            "background_music": {
                "style": "Upbeat, light, non-intrusive",
                "volume": "20-30% of voiceover volume",
                "genre": "Light jazz, acoustic, or ambient"
            },
            "sound_effects": {
                "cooking_sounds": "Subtle sizzling, chopping",
                "ambient": "Light restaurant atmosphere",
                "emphasis": "Soft transitions between sections"
            }
        }

    def _generate_production_notes(self) -> List[str]:
        """Generate production notes and tips"""
        return [
            "Ensure all food shots are well-lit and appetizing",
            "Keep text overlays readable and on-screen for adequate time",
            "Maintain consistent color grading throughout",
            "Use smooth transitions between scenes",
            "Include restaurant branding (logo, colors) subtly",
            "Ensure video works well both with and without sound",
            "Optimize for mobile viewing (vertical/square formats if needed)",
            "Include captions for accessibility"
        ]

    def _estimate_complexity(self, outline: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate production complexity"""
        visual_requirements = outline.get("visual_requirements", {})
        required_shots = len(visual_requirements.get("required_shots", []))
        available_footage = visual_requirements.get("available_footage", 0)

        complexity_score = 1.0

        # Increase complexity if more footage needed
        if required_shots > available_footage:
            complexity_score += 0.3

        # Increase complexity for audio requirements
        audio_requirements = outline.get("audio_requirements", {})
        if audio_requirements.get("sound_effects"):
            complexity_score += 0.2

        return {
            "score": complexity_score,
            "level": "Low" if complexity_score < 1.3 else "Medium" if complexity_score < 1.6 else "High",
            "multiplier": complexity_score
        }

    def _calculate_additional_footage_needed(self, footage_data: Dict[str, Any]) -> int:
        """Calculate how much additional footage might be needed"""
        available = len(footage_data.get("footage_suggestions", []))
        typical_needed = 8  # Typical number of clips for a good promotional video

        return max(0, typical_needed - available)