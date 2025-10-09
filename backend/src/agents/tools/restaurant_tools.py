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
        Extract comprehensive restaurant information from a Google Maps URL.

        This tool processes Google Maps URLs to extract detailed restaurant business information
        including contact details, ratings, and operational data using Google Places API.

        Args:
            google_maps_url (str): A valid Google Maps URL for the restaurant.
                                 Supports formats like:
                                 - https://maps.google.com/maps/place/Restaurant+Name/...
                                 - https://goo.gl/maps/shortened_url
                                 - URLs with coordinates or place IDs

        Returns:
            Dict[str, Any]: Restaurant information dictionary containing:
                - restaurant_name (str): Official business name
                - address (str): Full formatted address
                - website (str): Restaurant website URL (if available)
                - phone (str): Formatted phone number (if available)
                - rating (float): Google rating (0.0-5.0)
                - reviews_count (int): Total number of reviews
                - place_id (str): Google Places unique identifier
                - price_level (int): Price level indicator (1-4, if available)
                - opening_hours (List[str]): Weekly hours (if available)
                - error (str): Error message if extraction fails
        """
        try:
            # Validate Google Maps URL format
            if not google_maps_url or not isinstance(google_maps_url, str):
                return {"error": "Invalid input: google_maps_url must be a non-empty string"}

            if not any(domain in google_maps_url.lower() for domain in ['maps.google.', 'goo.gl/maps', 'maps.app.goo.gl']):
                return {"error": "Invalid URL: Must be a valid Google Maps URL"}

            logger.info(f"Processing Google Maps URL: {google_maps_url}")

            # Extract place info from URL
            place_info = self._extract_place_info_from_url(google_maps_url)

            if not place_info:
                return {"error": "Could not extract place information from the provided Google Maps URL. Please check the URL format."}

            # Get detailed information from Google Places API
            place_details = self._get_place_details(place_info)

            logger.info("Successfully extracted restaurant information")
            return place_details

        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}")
            return {"error": str(e)}

    def search_restaurant_by_name(self, restaurant_name: str, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for a restaurant by name with optional location filtering.

        This tool searches Google Places API to find restaurant information based on
        the restaurant name and optional location parameters. It returns the most
        relevant match with comprehensive business details.

        Args:
            restaurant_name (str): Name of the restaurant to search for.
                                 Can include partial names or common variations.
                                 Examples: "Joe's Pizza", "Starbucks", "McDonald's"
            location (str, optional): Geographic location to focus the search.
                                    Can be a city, address, neighborhood, or region.
                                    Examples: "New York, NY", "Downtown Seattle", "90210"

        Returns:
            Dict[str, Any]: Restaurant information dictionary containing:
                - restaurant_name (str): Official business name
                - address (str): Full formatted address
                - website (str): Restaurant website URL (if available)
                - phone (str): Formatted phone number (if available)
                - rating (float): Google rating (0.0-5.0)
                - reviews_count (int): Total number of reviews
                - place_id (str): Google Places unique identifier
                - price_level (int): Price level indicator (1-4, if available)
                - opening_hours (List[str]): Weekly hours (if available)
                - error (str): Error message if no restaurant found or search fails
        """
        try:
            # Validate input parameters
            if not restaurant_name or not isinstance(restaurant_name, str):
                return {"error": "Invalid input: restaurant_name must be a non-empty string"}

            restaurant_name = restaurant_name.strip()
            if len(restaurant_name) < 2:
                return {"error": "Invalid input: restaurant_name must be at least 2 characters long"}

            query = restaurant_name
            if location:
                if isinstance(location, str):
                    location = location.strip()
                    if location:
                        query += f" {location}"
                else:
                    return {"error": "Invalid input: location must be a string if provided"}

            logger.info(f"Searching for restaurant: '{query}'")

            places_result = self.google_maps_client.places(
                query=query,
                type="restaurant"
            )

            if not places_result["results"]:
                suggestion = f"Try searching with a different location or check the spelling of '{restaurant_name}'"
                return {"error": f"No restaurant found for '{restaurant_name}'. {suggestion}"}

            place_id = places_result["results"][0]["place_id"]
            return self._get_detailed_place_info(place_id)

        except Exception as e:
            logger.error(f"Error searching for restaurant: {str(e)}")
            return {"error": str(e)}

    def get_restaurant_details(self, place_id: str) -> Dict[str, Any]:
        """
        Retrieve comprehensive restaurant details using Google Places place_id.

        This tool fetches detailed restaurant information directly from Google Places API
        using a specific place_id. This is the most reliable method for getting accurate
        restaurant data when you already have the place identifier.

        Args:
            place_id (str): The Google Places unique place identifier.
                          Format: A textual identifier that uniquely identifies a place.
                          Example: "ChIJN1t_tDeuEmsRUsoyG83frY4"
                          Note: place_ids are returned by other Google Places API calls.

        Returns:
            Dict[str, Any]: Comprehensive restaurant information dictionary containing:
                - restaurant_name (str): Official business name
                - address (str): Full formatted address
                - website (str): Restaurant website URL (if available)
                - phone (str): Formatted phone number (if available)
                - rating (float): Google rating (0.0-5.0)
                - reviews_count (int): Total number of reviews
                - place_id (str): Google Places unique identifier (same as input)
                - price_level (int): Price level indicator (1-4, if available)
                - opening_hours (List[str]): Weekly operating hours (if available)
                - error (str): Error message if place_id is invalid or lookup fails
        """
        try:
            # Validate place_id parameter
            if not place_id or not isinstance(place_id, str):
                return {"error": "Invalid input: place_id must be a non-empty string"}

            place_id = place_id.strip()
            if len(place_id) < 10:  # Google place_ids are typically much longer
                return {"error": "Invalid place_id format: place_id appears to be too short"}

            logger.info(f"Fetching details for place_id: {place_id}")

            return self._get_detailed_place_info(place_id)
        except Exception as e:
            logger.error(f"Error getting restaurant details: {str(e)}")
            if "INVALID_REQUEST" in str(e):
                return {"error": f"Invalid place_id: '{place_id}' is not a valid Google Places identifier"}
            return {"error": f"Failed to retrieve restaurant details: {str(e)}"}

    def _extract_place_info_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract place ID or coordinates from Google Maps URL"""
        original_url = url

        # Handle shortened URLs by resolving them first
        if any(short_domain in url.lower() for short_domain in ['goo.gl/maps', 'maps.app.goo.gl']):
            try:
                logger.info(f"Resolving shortened URL: {url}")
                response = requests.head(url, allow_redirects=True, timeout=10)
                url = response.url
                logger.info(f"Resolved to: {url}")
            except Exception as e:
                logger.warning(f"Failed to resolve shortened URL {original_url}: {str(e)}")
                # Continue with original URL in case it still works
                url = original_url

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

