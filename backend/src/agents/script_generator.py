from typing import Dict, Any, List
import openai
from src.core.base_agent import BaseAgent

class ScriptGeneratorAgent(BaseAgent):
    """
    Creates promo script & scene plan using AI
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ScriptGeneratorAgent", config)
        openai.api_key = self.config.get("openai_api_key", "")
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate promotional script and scene plan
        
        Args:
            input_data: {
                "restaurant_name": str,
                "address": str,
                "menu": List[Dict],
                "style": str,  # luxury, casual, street_food
                "duration": int  # seconds
            }
            
        Returns:
            {
                "script": str,
                "scenes": [
                    {
                        "text": str,
                        "duration": float,
                        "image_prompt": str,
                        "voiceover_text": str
                    },
                    ...
                ],
                "total_duration": float,
                "style": str
            }
        """
        self.validate_input(input_data, ["restaurant_name", "menu", "style"])
        
        try:
            restaurant_name = input_data["restaurant_name"]
            menu = input_data["menu"]
            style = input_data["style"]
            duration = input_data.get("duration", 30)
            
            self.log_progress(f"Generating {style} script for {restaurant_name}")
            
            # Generate script using AI
            script_data = await self._generate_script(
                restaurant_name, menu, style, duration
            )
            
            # Create scene breakdown
            scenes = await self._create_scenes(script_data, duration)
            
            self.log_progress("Script generation completed")
            
            return {
                "script": script_data["script"],
                "scenes": scenes,
                "total_duration": duration,
                "style": style
            }
            
        except Exception as e:
            self.log_progress(f"Error generating script: {str(e)}", "error")
            raise
    
    async def _generate_script(self, restaurant_name: str, menu: List[Dict], 
                             style: str, duration: int) -> Dict[str, Any]:
        """
        Generate promotional script using OpenAI
        """
        # Extract menu highlights
        menu_highlights = self._extract_menu_highlights(menu)
        
        # Create style-specific prompt
        style_prompts = {
            "luxury": "elegant, sophisticated, premium dining experience",
            "casual": "friendly, welcoming, comfort food atmosphere",
            "street_food": "authentic, vibrant, bold flavors"
        }
        
        style_description = style_prompts.get(style, "welcoming and appetizing")
        
        prompt = f"""
        Create a {duration}-second promotional video script for {restaurant_name}.
        
        Style: {style_description}
        
        Menu highlights:
        {menu_highlights}
        
        Requirements:
        - Create engaging, {style_description} copy
        - Highlight the best menu items
        - Include a clear call-to-action
        - Write for voiceover (natural speech patterns)
        - Keep within {duration} seconds when read aloud
        - Focus on what makes this restaurant special
        
        Format the response as a natural, flowing script suitable for voiceover.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional marketing copywriter specializing in restaurant promotional content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            script = response.choices[0].message.content.strip()
            
            return {"script": script}
            
        except Exception as e:
            self.log_progress(f"AI script generation failed: {str(e)}", "warning")
            return self._generate_fallback_script(restaurant_name, menu_highlights, style)
    
    def _extract_menu_highlights(self, menu: List[Dict]) -> str:
        """
        Extract key menu items for script generation
        """
        highlights = []
        
        for category in menu:
            category_name = category.get("category", "")
            items = category.get("items", [])
            
            # Take first 2 items from each category
            for item in items[:2]:
                name = item.get("name", "")
                description = item.get("description", "")
                if name:
                    if description:
                        highlights.append(f"{name}: {description}")
                    else:
                        highlights.append(name)
        
        return "\n".join(highlights[:8])  # Limit to 8 items
    
    async def _create_scenes(self, script_data: Dict[str, Any], 
                           total_duration: int) -> List[Dict[str, Any]]:
        """
        Break script into scenes with visual and timing information
        """
        script = script_data["script"]
        
        # Split script into sentences
        sentences = [s.strip() + "." for s in script.split(".") if s.strip()]
        
        # Calculate duration per scene
        num_scenes = len(sentences)
        scene_duration = total_duration / num_scenes if num_scenes > 0 else total_duration
        
        scenes = []
        
        for i, sentence in enumerate(sentences):
            # Generate image prompt based on content
            image_prompt = self._generate_image_prompt(sentence, i)
            
            scene = {
                "text": sentence,
                "duration": scene_duration,
                "image_prompt": image_prompt,
                "voiceover_text": sentence
            }
            scenes.append(scene)
        
        return scenes
    
    def _generate_image_prompt(self, text: str, scene_index: int) -> str:
        """
        Generate appropriate image prompt for scene content
        """
        text_lower = text.lower()
        
        # Map content to visual themes
        if scene_index == 0 or "welcome" in text_lower or "visit" in text_lower:
            return "restaurant exterior, welcoming entrance, warm lighting"
        elif "menu" in text_lower or "dish" in text_lower or any(food in text_lower for food in ["pasta", "pizza", "burger", "salad", "chicken", "fish"]):
            return "beautifully plated signature dish, professional food photography"
        elif "atmosphere" in text_lower or "dining" in text_lower:
            return "elegant restaurant interior, cozy dining atmosphere"
        elif "fresh" in text_lower or "ingredient" in text_lower:
            return "fresh ingredients, chef preparing food in kitchen"
        else:
            return "restaurant dining room, happy customers enjoying meal"
    
    def _generate_fallback_script(self, restaurant_name: str, 
                                menu_highlights: str, style: str) -> Dict[str, Any]:
        """
        Generate fallback script when AI fails
        """
        style_templates = {
            "luxury": f"Experience culinary excellence at {restaurant_name}. Our chef-crafted dishes featuring {menu_highlights} deliver an unforgettable fine dining experience. Reserve your table today for an evening of exceptional cuisine.",
            
            "casual": f"Welcome to {restaurant_name}, where great food brings people together. Enjoy our delicious {menu_highlights} in a warm, friendly atmosphere. Come hungry, leave happy. Visit us today!",
            
            "street_food": f"Taste the authentic flavors at {restaurant_name}! Our bold, fresh {menu_highlights} pack incredible taste into every bite. Real food, real flavor, real good. Stop by and taste the difference!"
        }
        
        script = style_templates.get(style, style_templates["casual"])
        
        return {"script": script}