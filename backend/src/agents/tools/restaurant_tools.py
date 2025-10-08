from typing import Dict, Any, Optional
import re
import googlemaps
import requests
from bs4 import BeautifulSoup
from agno.tools import Toolkit
import os
import logging

logger = logging.getLogger(__name__)

class RestaurantDataTools(Toolkit):
    """
    Tools for extracting restaurant information from Google Maps URLs
    """

    def __init__(self, google_places_api_key: Optional[str] = None):
        self.api_key = google_places_api_key or os.getenv("GOOGLE_PLACES_API_KEY", "")

        if not self.api_key or not self.api_key.startswith("AIza") or len(self.api_key) < 30:
            raise ValueError("Valid Google Places API key is required for RestaurantDataTools")

        self.google_maps_client = googlemaps.Client(key=self.api_key)
        logger.info("Google Maps client initialized successfully")

        super().__init__(
            name="RestaurantDataTools",
            tools=[
                self.extract_restaurant_from_maps_url,
                self.search_restaurant_by_name,
                self.get_restaurant_details
            ]
        )

    def extract_restaurant_from_maps_url(self, google_maps_url: str) -> Dict[str, Any]:
        """
        Extract restaurant information from a Google Maps URL.

        Args:
            google_maps_url (str): The Google Maps URL for the restaurant

        Returns:
            Dict with restaurant name, address, website, phone, rating, and reviews count
        """
        try:
            logger.info(f"Processing Google Maps URL: {google_maps_url}")

            # Extract place info from URL
            place_info = self._extract_place_info_from_url(google_maps_url)

            if not place_info:
                return {"error": "Could not extract place information from URL"}

            # Get detailed information from Google Places API
            place_details = self._get_place_details(place_info)

            logger.info("Successfully extracted restaurant information")
            return place_details

        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}")
            return {"error": str(e)}

    def search_restaurant_by_name(self, restaurant_name: str, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for a restaurant by name and optional location.

        Args:
            restaurant_name (str): Name of the restaurant to search for
            location (str, optional): Location to search in (city, address, etc.)

        Returns:
            Dict with restaurant information
        """
        try:
            query = restaurant_name
            if location:
                query += f" {location}"

            places_result = self.google_maps_client.places(
                query=query,
                type="restaurant"
            )

            if not places_result["results"]:
                return {"error": f"No restaurant found for '{restaurant_name}'"}

            place_id = places_result["results"][0]["place_id"]
            return self._get_detailed_place_info(place_id)

        except Exception as e:
            logger.error(f"Error searching for restaurant: {str(e)}")
            return {"error": str(e)}

    def get_restaurant_details(self, place_id: str) -> Dict[str, Any]:
        """
        Get detailed restaurant information using a Google Places place_id.

        Args:
            place_id (str): The Google Places place_id

        Returns:
            Dict with detailed restaurant information
        """
        try:
            return self._get_detailed_place_info(place_id)
        except Exception as e:
            logger.error(f"Error getting restaurant details: {str(e)}")
            return {"error": str(e)}

    def _extract_place_info_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract place ID or coordinates from Google Maps URL"""
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

    def _get_place_details(self, place_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed place information from Google Places API"""
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

        return self._get_detailed_place_info(place_id)

    def _get_detailed_place_info(self, place_id: str) -> Dict[str, Any]:
        """Get detailed information using place_id"""
        details = self.google_maps_client.place(
            place_id=place_id,
            fields=[
                "name", "formatted_address", "website",
                "formatted_phone_number", "rating", "user_ratings_total",
                "opening_hours", "price_level"
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
            "place_id": place_id,
            "price_level": place.get("price_level"),
            "opening_hours": place.get("opening_hours", {}).get("weekday_text", [])
        }

