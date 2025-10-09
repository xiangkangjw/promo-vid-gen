from typing import Dict, Any, List, Optional
import re
import requests
import os
from agno.tools import Toolkit
import logging
from firecrawl import Firecrawl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class MenuExtractionTools(Toolkit):
    """
    Tools for extracting menu information from restaurant websites using Firecrawl
    """

    def __init__(self):
        # Initialize Firecrawl client
        try:
            api_key = os.getenv("FIRECRAWL_API_KEY")
            if not api_key:
                raise ValueError("FIRECRAWL_API_KEY environment variable is required")

            self.firecrawl_client = Firecrawl(api_key=api_key)
            logger.info("Firecrawl client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firecrawl: {str(e)}")
            self.firecrawl_client = None
        super().__init__(
            name="MenuExtractionTools",
            tools=[
                self.extract_menu_from_website
            ]
        )

    def extract_menu_from_website(self, website_url: str) -> Dict[str, Any]:
        """
        Extract menu information from a restaurant website URL using Firecrawl.

        This tool uses Firecrawl's AI-powered extraction to intelligently identify
        and extract menu items, prices, descriptions, and categories from restaurant websites.
        It handles JavaScript-heavy sites and complex layouts automatically.

        Args:
            website_url (str): The restaurant's website URL.
                              Must be a valid HTTP/HTTPS URL.
                              Examples: "https://restaurant.com", "https://restaurant.com/menu"

        Returns:
            Dict[str, Any]: Extraction result containing:
                - success (bool): Whether extraction was successful
                - markdown_content (str): Raw markdown content from the website
                - content_length (int): Length of extracted content in characters
                - extraction_method (str): Method used for extraction ("firecrawl")
                - url (str): The URL that was scraped
                - error (str): Error message if extraction fails
        """
        try:
            # Validate input
            if not website_url or not isinstance(website_url, str):
                return {"error": "Invalid input: website_url must be a non-empty string"}

            website_url = website_url.strip()
            if not website_url:
                return {"error": "Invalid input: website_url cannot be empty"}

            # Validate URL format
            if not any(website_url.lower().startswith(protocol) for protocol in ['http://', 'https://']):
                return {"error": "Invalid URL: Must start with http:// or https://"}

            if len(website_url) < 10:
                return {"error": "Invalid URL: URL appears to be too short"}

            logger.info(f"Extracting menu from: {website_url}")

            # Use Firecrawl for AI-powered menu extraction
            menu_data = self._extract_with_firecrawl(website_url)

            logger.info(f"Successfully extracted content, length: {menu_data.get('content_length', 0)} characters")
            return menu_data

        except Exception as e:
            logger.error(f"Error extracting menu from {website_url}: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to extract menu: {str(e)}",
                "extraction_method": "failed",
                "url": website_url
            }


    def _extract_with_firecrawl(self, url: str) -> Dict[str, Any]:
        """Extract menu using Firecrawl AI-powered extraction"""
        try:
            # Check if Firecrawl client is available
            if not self.firecrawl_client:
                return {
                    "success": False,
                    "error": "Firecrawl client not available. Check API key and installation.",
                    "extraction_method": "failed",
                    "url": url
                }

            logger.info(f"Starting Firecrawl extraction for URL: {url}")

            # Extract menu data using Firecrawl v2 API
            result = self.firecrawl_client.scrape(
                url=url,
                formats=['markdown'],
                only_main_content=True,
                include_tags=['div', 'section', 'article', 'ul', 'li', 'table'],
                exclude_tags=['nav', 'footer', 'header', 'aside']
            )

            logger.info(f"Firecrawl API response type: {type(result)}")

            # Check if the result contains data (v2 API returns Document object)
            if not result:
                return {
                    "success": False,
                    "error": "Firecrawl extraction failed - no response received",
                    "extraction_method": "failed",
                    "url": url
                }

            # Get markdown content from Document object
            markdown_content = ""
            if hasattr(result, 'markdown') and result.markdown:
                markdown_content = result.markdown
            elif isinstance(result, dict) and result.get('markdown'):
                markdown_content = result.get('markdown', '')
            else:
                logger.warning(f"Firecrawl response structure: {result}")
                return {
                    "success": False,
                    "error": "Firecrawl extraction failed - no markdown content returned",
                    "extraction_method": "failed",
                    "url": url
                }

            logger.info(f"Extracted markdown content length: {len(markdown_content)} characters")

            return {
                "success": True,
                "markdown_content": markdown_content,
                "content_length": len(markdown_content),
                "extraction_method": "firecrawl",
                "url": url
            }

        except Exception as e:
            logger.error(f"Firecrawl extraction failed: {str(e)}")
            return {
                "success": False,
                "error": f"Firecrawl extraction failed: {str(e)}",
                "extraction_method": "failed",
                "url": url
            }

