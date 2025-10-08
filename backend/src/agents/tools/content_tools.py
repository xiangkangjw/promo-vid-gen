from typing import Dict, Any, List
from agno.tools import Toolkit
import logging

logger = logging.getLogger(__name__)

class ContentGenerationTools(Toolkit):
    """
    Tools for generating video scripts and content
    """

    def __init__(self):
        super().__init__(
            name="ContentGenerationTools",
            tools=[
                self.generate_video_script,
                self.create_promotional_copy,
                self.suggest_video_styles,
                self.optimize_script_length
            ]
        )

    def generate_video_script(self, restaurant_data: Dict[str, Any], menu_data: Dict[str, Any], style: str = "casual") -> Dict[str, Any]:
        """
        Generate a video script based on restaurant and menu data.

        Args:
            restaurant_data (dict): Restaurant information (name, address, etc.)
            menu_data (dict): Menu information and analysis
            style (str): Script style (casual, professional, trendy, etc.)

        Returns:
            Dict with generated script sections and timing
        """
        try:
            # This function helps the AI agent understand what data is available
            # The actual script generation will be done by the AI agent using this data

            available_data = {
                "restaurant_info": {
                    "name": restaurant_data.get("restaurant_name", ""),
                    "rating": restaurant_data.get("rating", 0),
                    "reviews_count": restaurant_data.get("reviews_count", 0),
                    "address": restaurant_data.get("address", ""),
                    "phone": restaurant_data.get("phone", ""),
                    "website": restaurant_data.get("website", "")
                },
                "menu_highlights": {
                    "total_items": menu_data.get("total_items", 0),
                    "price_range": menu_data.get("analysis", {}).get("price_range", {}),
                    "popular_items": menu_data.get("analysis", {}).get("popular_items", []),
                    "categories": menu_data.get("analysis", {}).get("categories", []),
                    "dietary_options": menu_data.get("analysis", {}).get("dietary_options", {})
                },
                "script_requirements": {
                    "style": style,
                    "target_duration": "30-60 seconds",
                    "tone": self._get_tone_for_style(style),
                    "key_points": self._get_key_points_template()
                }
            }

            return {
                "status": "data_prepared",
                "available_data": available_data,
                "message": "Data prepared for script generation. The AI agent will now create the actual script."
            }

        except Exception as e:
            logger.error(f"Error preparing script data: {str(e)}")
            return {"error": str(e)}

    def create_promotional_copy(self, restaurant_data: Dict[str, Any], target_audience: str = "general") -> Dict[str, Any]:
        """
        Create promotional copy for social media and marketing.

        Args:
            restaurant_data (dict): Restaurant information
            target_audience (str): Target audience (general, families, young_adults, etc.)

        Returns:
            Dict with promotional copy variations
        """
        try:
            copy_data = {
                "restaurant_name": restaurant_data.get("restaurant_name", ""),
                "rating": restaurant_data.get("rating", 0),
                "unique_selling_points": self._extract_selling_points(restaurant_data),
                "target_audience": target_audience,
                "copy_requirements": {
                    "lengths": ["short (under 50 chars)", "medium (50-100 chars)", "long (100+ chars)"],
                    "platforms": ["instagram", "facebook", "twitter", "tiktok"],
                    "call_to_actions": ["visit_now", "call_today", "order_online", "book_table"]
                }
            }

            return {
                "status": "copy_data_prepared",
                "copy_data": copy_data,
                "message": "Data prepared for promotional copy generation."
            }

        except Exception as e:
            logger.error(f"Error preparing promotional copy data: {str(e)}")
            return {"error": str(e)}

    def suggest_video_styles(self, restaurant_data: Dict[str, Any], menu_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest appropriate video styles based on restaurant type and menu.

        Args:
            restaurant_data (dict): Restaurant information
            menu_data (dict): Menu information

        Returns:
            Dict with suggested video styles and their characteristics
        """
        try:
            restaurant_types = restaurant_data.get("restaurant_types", [])
            price_range = menu_data.get("analysis", {}).get("price_range", {})

            style_suggestions = self._analyze_appropriate_styles(restaurant_types, price_range)

            return {
                "suggested_styles": style_suggestions,
                "restaurant_analysis": {
                    "types": restaurant_types,
                    "price_level": restaurant_data.get("price_level"),
                    "rating": restaurant_data.get("rating", 0)
                }
            }

        except Exception as e:
            logger.error(f"Error suggesting video styles: {str(e)}")
            return {"error": str(e)}

    def optimize_script_length(self, script_data: Dict[str, Any], target_duration: int = 45) -> Dict[str, Any]:
        """
        Optimize script length for target video duration.

        Args:
            script_data (dict): Script content to optimize
            target_duration (int): Target duration in seconds

        Returns:
            Dict with optimization suggestions
        """
        try:
            optimization_guidelines = {
                "target_duration": target_duration,
                "words_per_second": 2.5,  # Average speaking pace
                "target_word_count": int(target_duration * 2.5),
                "section_timing": {
                    "intro": f"0-{target_duration * 0.2:.0f}s",
                    "main_content": f"{target_duration * 0.2:.0f}-{target_duration * 0.8:.0f}s",
                    "call_to_action": f"{target_duration * 0.8:.0f}-{target_duration}s"
                },
                "optimization_tips": [
                    "Keep sentences short and punchy",
                    "Focus on 2-3 key selling points maximum",
                    "Use active voice",
                    "Include clear call-to-action",
                    "Leave pauses for visual elements"
                ]
            }

            return {
                "optimization_guidelines": optimization_guidelines,
                "status": "guidelines_provided"
            }

        except Exception as e:
            logger.error(f"Error creating optimization guidelines: {str(e)}")
            return {"error": str(e)}

    def _get_tone_for_style(self, style: str) -> str:
        """Get appropriate tone for given style"""
        tone_mapping = {
            "casual": "Friendly, approachable, conversational",
            "professional": "Polished, trustworthy, authoritative",
            "trendy": "Hip, modern, energetic",
            "elegant": "Sophisticated, refined, upscale",
            "fun": "Playful, exciting, enthusiastic",
            "family": "Warm, welcoming, inclusive"
        }
        return tone_mapping.get(style, "Friendly and engaging")

    def _get_key_points_template(self) -> List[str]:
        """Get template for key points to include in script"""
        return [
            "Restaurant name and location",
            "Unique selling proposition",
            "Popular menu items or specialties",
            "Atmosphere/ambiance",
            "Customer ratings/reviews",
            "Call to action (visit, call, order)"
        ]

    def _extract_selling_points(self, restaurant_data: Dict[str, Any]) -> List[str]:
        """Extract unique selling points from restaurant data"""
        selling_points = []

        # High rating
        rating = restaurant_data.get("rating", 0)
        if rating >= 4.5:
            selling_points.append(f"Highly rated ({rating}/5 stars)")
        elif rating >= 4.0:
            selling_points.append(f"Great reviews ({rating}/5 stars)")

        # Review count
        reviews_count = restaurant_data.get("reviews_count", 0)
        if reviews_count > 500:
            selling_points.append(f"Trusted by {reviews_count}+ customers")

        # Restaurant types
        types = restaurant_data.get("restaurant_types", [])
        if "meal_delivery" in types:
            selling_points.append("Delivery available")
        if "meal_takeaway" in types:
            selling_points.append("Takeaway available")

        return selling_points

    def _analyze_appropriate_styles(self, restaurant_types: List[str], price_range: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze and suggest appropriate video styles"""
        styles = []

        avg_price = price_range.get("avg_price", 0)

        # Budget-friendly styles
        if avg_price < 15:
            styles.append({
                "style": "casual",
                "description": "Friendly, approachable, everyday dining",
                "characteristics": ["Conversational tone", "Focus on value", "Comfort food emphasis"]
            })
            styles.append({
                "style": "fun",
                "description": "Energetic, exciting, great for families",
                "characteristics": ["Upbeat music", "Vibrant visuals", "Community feel"]
            })

        # Mid-range styles
        elif avg_price < 35:
            styles.append({
                "style": "professional",
                "description": "Quality-focused, reliable dining experience",
                "characteristics": ["Polished presentation", "Quality emphasis", "Service highlights"]
            })
            styles.append({
                "style": "trendy",
                "description": "Modern, hip, Instagram-worthy",
                "characteristics": ["Contemporary music", "Stylish visuals", "Social media friendly"]
            })

        # Upscale styles
        else:
            styles.append({
                "style": "elegant",
                "description": "Sophisticated, refined dining experience",
                "characteristics": ["Classical music", "Premium visuals", "Luxury emphasis"]
            })
            styles.append({
                "style": "professional",
                "description": "High-quality, exceptional service",
                "characteristics": ["Premium presentation", "Chef expertise", "Fine dining experience"]
            })

        # Always add family-friendly if applicable
        if any(ftype in restaurant_types for ftype in ["family", "casual_dining"]):
            styles.append({
                "style": "family",
                "description": "Warm, welcoming, family-oriented",
                "characteristics": ["Inclusive messaging", "Family values", "Comfort atmosphere"]
            })

        return styles[:3]  # Return top 3 suggestions