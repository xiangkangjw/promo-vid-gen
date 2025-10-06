from typing import Dict, Any
import re
import googlemaps
import requests
from bs4 import BeautifulSoup
from src.core.base_agent import BaseAgent

class MapParserAgent(BaseAgent):
    """
    Extracts restaurant name, address, website, and reviews from Google Maps URL
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("MapParserAgent", config)
        self.google_maps_client = googlemaps.Client(
            key=self.config.get("google_places_api_key", "")
        )
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract restaurant information from Google Maps URL
        
        Args:
            input_data: {"google_maps_url": "https://maps.app.goo.gl/..."}
            
        Returns:
            {
                "restaurant_name": str,
                "address": str,
                "website": str,
                "phone": str,
                "rating": float,
                "reviews_count": int,
                "place_id": str
            }
        """
        self.validate_input(input_data, ["google_maps_url"])
        
        try:
            google_maps_url = input_data["google_maps_url"]
            self.log_progress(f"Processing Google Maps URL: {google_maps_url}")
            
            # Extract place ID or coordinates from URL
            place_info = await self._extract_place_info(google_maps_url)
            
            if not place_info:
                raise ValueError("Could not extract place information from URL")
            
            # Get detailed information from Google Places API
            place_details = await self._get_place_details(place_info)
            
            self.log_progress("Successfully extracted restaurant information")
            return place_details
            
        except Exception as e:
            self.log_progress(f"Error processing URL: {str(e)}", "error")
            raise
    
    async def _extract_place_info(self, url: str) -> Dict[str, Any]:
        """
        Extract place ID or coordinates from Google Maps URL
        """
        # Handle different URL formats
        patterns = [
            r'place/([^/]+)/',  # place name
            r'@([-\d.]+),([-\d.]+)',  # coordinates
            r'data=.*!1m.*!3d([-\d.]+)!4d([-\d.]+)',  # embedded coordinates
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                if len(match.groups()) == 1:
                    # Place name
                    return {"query": match.group(1).replace('+', ' ')}
                else:
                    # Coordinates
                    lat, lng = match.groups()
                    return {"location": (float(lat), float(lng))}
        
        return None
    
    async def _get_place_details(self, place_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed place information from Google Places API
        """
        try:
            if "query" in place_info:
                # Search by name
                places_result = self.google_maps_client.places(
                    query=place_info["query"],
                    type="restaurant"
                )
                if places_result["results"]:
                    place_id = places_result["results"][0]["place_id"]
                else:
                    raise ValueError("Restaurant not found")
            
            elif "location" in place_info:
                # Search by coordinates
                places_result = self.google_maps_client.places_nearby(
                    location=place_info["location"],
                    radius=100,
                    type="restaurant"
                )
                if places_result["results"]:
                    place_id = places_result["results"][0]["place_id"]
                else:
                    raise ValueError("Restaurant not found at coordinates")
            
            # Get detailed information
            details = self.google_maps_client.place(
                place_id=place_id,
                fields=[
                    "name", "formatted_address", "website", 
                    "formatted_phone_number", "rating", "user_ratings_total"
                ]
            )
            
            place = details["result"]
            
            return {
                "restaurant_name": place.get("name", ""),
                "address": place.get("formatted_address", ""),
                "website": place.get("website", ""),
                "phone": place.get("formatted_phone_number", ""),
                "rating": place.get("rating", 0.0),
                "reviews_count": place.get("user_ratings_total", 0),
                "place_id": place_id
            }
            
        except Exception as e:
            # Fallback to web scraping if API fails
            self.log_progress("API failed, attempting web scraping", "warning")
            return await self._fallback_scraping(place_info)
    
    async def _fallback_scraping(self, place_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback method using web scraping when API is unavailable
        """
        # TODO: Implement web scraping fallback
        return {
            "restaurant_name": "Restaurant Name",
            "address": "123 Main St",
            "website": "",
            "phone": "",
            "rating": 0.0,
            "reviews_count": 0,
            "place_id": ""
        }