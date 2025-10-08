from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from agno.tools import Toolkit
import logging
import asyncio

logger = logging.getLogger(__name__)

class MenuExtractionTools(Toolkit):
    """
    Tools for extracting menu information from restaurant websites
    """

    def __init__(self):
        super().__init__(
            name="MenuExtractionTools",
            tools=[
                self.extract_menu_from_website,
                self.scrape_menu_with_playwright,
                self.analyze_menu_structure
            ]
        )

    def extract_menu_from_website(self, website_url: str) -> Dict[str, Any]:
        """
        Extract menu information from a restaurant website URL.

        Args:
            website_url (str): The restaurant's website URL

        Returns:
            Dict with menu items, categories, prices, and descriptions
        """
        try:
            logger.info(f"Extracting menu from: {website_url}")

            if not website_url or website_url == "":
                return {"error": "No website URL provided"}

            # Try simple HTTP request first
            menu_data = self._simple_menu_extraction(website_url)

            if not menu_data.get("menu_items"):
                # Fallback to Playwright for dynamic content
                logger.info("Simple extraction failed, trying Playwright")
                menu_data = asyncio.run(self._playwright_menu_extraction(website_url))

            return menu_data

        except Exception as e:
            logger.error(f"Error extracting menu: {str(e)}")
            return {"error": str(e)}

    def scrape_menu_with_playwright(self, website_url: str) -> Dict[str, Any]:
        """
        Extract menu using Playwright for JavaScript-heavy sites.

        Args:
            website_url (str): The restaurant's website URL

        Returns:
            Dict with menu information extracted via browser automation
        """
        try:
            return asyncio.run(self._playwright_menu_extraction(website_url))
        except Exception as e:
            logger.error(f"Playwright extraction failed: {str(e)}")
            return {"error": str(e)}

    def analyze_menu_structure(self, menu_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and categorize extracted menu data.

        Args:
            menu_data (dict): Raw menu data to analyze

        Returns:
            Dict with structured menu analysis including categories, price ranges, etc.
        """
        try:
            if "menu_items" not in menu_data or not menu_data["menu_items"]:
                return {"error": "No menu items to analyze"}

            menu_items = menu_data["menu_items"]

            analysis = {
                "total_items": len(menu_items),
                "categories": self._extract_categories(menu_items),
                "price_range": self._calculate_price_range(menu_items),
                "popular_items": self._identify_popular_items(menu_items),
                "dietary_options": self._identify_dietary_options(menu_items)
            }

            return {
                "analysis": analysis,
                "structured_menu": self._structure_menu_by_category(menu_items)
            }

        except Exception as e:
            logger.error(f"Error analyzing menu: {str(e)}")
            return {"error": str(e)}

    def _simple_menu_extraction(self, url: str) -> Dict[str, Any]:
        """Extract menu using simple HTTP requests and BeautifulSoup"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Common menu selectors
            menu_selectors = [
                '.menu-item', '.menu-section', '.food-item',
                '[class*="menu"]', '[id*="menu"]',
                '.dish', '.product', '.item'
            ]

            menu_items = []

            for selector in menu_selectors:
                items = soup.select(selector)
                if items and len(items) > 2:  # Found likely menu items
                    for item in items:
                        menu_item = self._parse_menu_item(item)
                        if menu_item:
                            menu_items.append(menu_item)
                    break

            return {
                "menu_items": menu_items,
                "extraction_method": "simple_http",
                "total_items": len(menu_items)
            }

        except Exception as e:
            logger.warning(f"Simple extraction failed: {str(e)}")
            return {"menu_items": [], "error": str(e)}

    async def _playwright_menu_extraction(self, url: str) -> Dict[str, Any]:
        """Extract menu using Playwright for dynamic content"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await page.goto(url, wait_until="networkidle")
                await page.wait_for_timeout(3000)  # Wait for dynamic content

                # Try to find and click menu links
                menu_triggers = ['menu', 'food', 'dishes', 'order']
                for trigger in menu_triggers:
                    try:
                        await page.click(f'a[href*="{trigger}"], button:has-text("{trigger}")', timeout=2000)
                        await page.wait_for_timeout(2000)
                        break
                    except:
                        continue

                # Extract menu items
                menu_items = await page.evaluate("""
                    () => {
                        const items = [];
                        const selectors = [
                            '.menu-item', '.menu-section', '.food-item',
                            '[class*="menu"]', '[id*="menu"]',
                            '.dish', '.product', '.item'
                        ];

                        for (const selector of selectors) {
                            const elements = document.querySelectorAll(selector);
                            if (elements.length > 2) {
                                elements.forEach(el => {
                                    const name = el.querySelector('h1, h2, h3, h4, .title, .name')?.textContent?.trim();
                                    const price = el.textContent.match(/\\$[\\d,]+(?:\\.\\d{2})?/)?.[0];
                                    const description = el.querySelector('p, .description, .desc')?.textContent?.trim();

                                    if (name) {
                                        items.push({
                                            name: name,
                                            price: price || 'Price not available',
                                            description: description || '',
                                            category: 'General'
                                        });
                                    }
                                });
                                break;
                            }
                        }
                        return items;
                    }
                """)

                await browser.close()

                return {
                    "menu_items": menu_items,
                    "extraction_method": "playwright",
                    "total_items": len(menu_items)
                }

        except Exception as e:
            logger.error(f"Playwright extraction failed: {str(e)}")
            return {"menu_items": [], "error": str(e)}

    def _parse_menu_item(self, item_element) -> Optional[Dict[str, str]]:
        """Parse a menu item from HTML element"""
        try:
            # Extract name
            name_selectors = ['h1', 'h2', 'h3', 'h4', '.title', '.name', '.dish-name']
            name = None
            for selector in name_selectors:
                name_elem = item_element.select_one(selector)
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    break

            if not name:
                name = item_element.get_text(strip=True)[:50]  # Fallback

            # Extract price
            price_text = item_element.get_text()
            price_match = None
            import re
            price_patterns = [r'\$[\d,]+(?:\.\d{2})?', r'[\d,]+(?:\.\d{2})?\s*\$']
            for pattern in price_patterns:
                match = re.search(pattern, price_text)
                if match:
                    price_match = match.group()
                    break

            # Extract description
            desc_selectors = ['p', '.description', '.desc', '.details']
            description = ""
            for selector in desc_selectors:
                desc_elem = item_element.select_one(selector)
                if desc_elem:
                    description = desc_elem.get_text(strip=True)
                    break

            return {
                "name": name,
                "price": price_match or "Price not available",
                "description": description,
                "category": "General"
            }

        except Exception as e:
            logger.warning(f"Error parsing menu item: {str(e)}")
            return None

    def _extract_categories(self, menu_items: List[Dict]) -> List[str]:
        """Extract unique categories from menu items"""
        categories = set()
        for item in menu_items:
            if item.get("category"):
                categories.add(item["category"])
        return list(categories) if categories else ["General"]

    def _calculate_price_range(self, menu_items: List[Dict]) -> Dict[str, Any]:
        """Calculate price range from menu items"""
        prices = []
        import re

        for item in menu_items:
            price_text = item.get("price", "")
            price_match = re.search(r'[\d,]+(?:\.\d{2})?', price_text)
            if price_match:
                try:
                    price = float(price_match.group().replace(',', ''))
                    prices.append(price)
                except:
                    continue

        if prices:
            return {
                "min_price": min(prices),
                "max_price": max(prices),
                "avg_price": sum(prices) / len(prices)
            }
        else:
            return {"min_price": 0, "max_price": 0, "avg_price": 0}

    def _identify_popular_items(self, menu_items: List[Dict]) -> List[str]:
        """Identify potentially popular items based on descriptions"""
        popular_keywords = ["popular", "favorite", "signature", "special", "best", "recommended"]
        popular_items = []

        for item in menu_items:
            description = item.get("description", "").lower()
            name = item.get("name", "").lower()

            if any(keyword in description or keyword in name for keyword in popular_keywords):
                popular_items.append(item["name"])

        return popular_items[:5]  # Return top 5

    def _identify_dietary_options(self, menu_items: List[Dict]) -> Dict[str, List[str]]:
        """Identify dietary options from menu items"""
        dietary_keywords = {
            "vegetarian": ["vegetarian", "veggie", "veg"],
            "vegan": ["vegan"],
            "gluten_free": ["gluten-free", "gluten free", "gf"],
            "dairy_free": ["dairy-free", "dairy free"],
            "spicy": ["spicy", "hot", "chili"]
        }

        dietary_options = {key: [] for key in dietary_keywords}

        for item in menu_items:
            text = f"{item.get('name', '')} {item.get('description', '')}".lower()

            for diet_type, keywords in dietary_keywords.items():
                if any(keyword in text for keyword in keywords):
                    dietary_options[diet_type].append(item["name"])

        return {k: v for k, v in dietary_options.items() if v}  # Only return non-empty lists

    def _structure_menu_by_category(self, menu_items: List[Dict]) -> Dict[str, List[Dict]]:
        """Structure menu items by category"""
        structured = {}

        for item in menu_items:
            category = item.get("category", "General")
            if category not in structured:
                structured[category] = []
            structured[category].append(item)

        return structured