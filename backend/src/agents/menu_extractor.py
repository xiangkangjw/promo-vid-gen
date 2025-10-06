from typing import Dict, Any, List
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from src.core.base_agent import BaseAgent

class MenuExtractorAgent(BaseAgent):
    """
    Crawls website or PDF to extract menu items
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("MenuExtractorAgent", config)
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract menu items from restaurant website
        
        Args:
            input_data: {
                "website": "https://restaurant.com",
                "restaurant_name": "Restaurant Name"
            }
            
        Returns:
            {
                "menu": [
                    {
                        "category": "Starters",
                        "items": [
                            {"name": "Bruschetta", "price": "$12", "description": "..."},
                            ...
                        ]
                    },
                    ...
                ],
                "extraction_method": "website|pdf|fallback"
            }
        """
        self.validate_input(input_data, ["website", "restaurant_name"])
        
        try:
            website = input_data["website"]
            restaurant_name = input_data["restaurant_name"]
            
            self.log_progress(f"Extracting menu from: {website}")
            
            # Try different extraction methods
            menu_data = None
            extraction_method = "fallback"
            
            if website:
                # First try website extraction
                menu_data = await self._extract_from_website(website)
                if menu_data:
                    extraction_method = "website"
                
                # If website fails, try PDF extraction
                if not menu_data:
                    menu_data = await self._extract_from_pdf(website)
                    if menu_data:
                        extraction_method = "pdf"
            
            # Fallback to sample menu
            if not menu_data:
                self.log_progress("Using fallback sample menu", "warning")
                menu_data = self._generate_fallback_menu(restaurant_name)
            
            self.log_progress(f"Menu extraction completed using {extraction_method}")
            
            return {
                "menu": menu_data,
                "extraction_method": extraction_method
            }
            
        except Exception as e:
            self.log_progress(f"Error extracting menu: {str(e)}", "error")
            raise
    
    async def _extract_from_website(self, website: str) -> List[Dict[str, Any]]:
        """
        Extract menu from restaurant website using web scraping
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                
                await page.goto(website)
                await page.wait_for_load_state('networkidle')
                
                # Common menu selectors
                menu_selectors = [
                    '.menu', '#menu', '.food-menu', '.restaurant-menu',
                    '[class*="menu"]', '[id*="menu"]'
                ]
                
                menu_items = []
                
                for selector in menu_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        if elements:
                            menu_items = await self._parse_menu_elements(page, elements)
                            if menu_items:
                                break
                    except:
                        continue
                
                await browser.close()
                
                return self._structure_menu_data(menu_items)
                
        except Exception as e:
            self.log_progress(f"Website extraction failed: {str(e)}", "warning")
            return None
    
    async def _extract_from_pdf(self, website: str) -> List[Dict[str, Any]]:
        """
        Extract menu from PDF links found on the website
        """
        try:
            # Look for PDF links on the website
            async with aiohttp.ClientSession() as session:
                async with session.get(website) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find PDF links
                    pdf_links = []
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.endswith('.pdf') or 'menu' in href.lower():
                            if not href.startswith('http'):
                                href = f"{website.rstrip('/')}/{href.lstrip('/')}"
                            pdf_links.append(href)
                    
                    # TODO: Implement PDF OCR extraction
                    # For now, return None to trigger fallback
                    return None
                    
        except Exception as e:
            self.log_progress(f"PDF extraction failed: {str(e)}", "warning")
            return None
    
    async def _parse_menu_elements(self, page, elements) -> List[Dict[str, Any]]:
        """
        Parse menu elements from the webpage
        """
        menu_items = []
        
        for element in elements:
            try:
                # Extract text content
                text = await element.text_content()
                if text and len(text) > 50:  # Likely contains menu items
                    
                    # Look for item patterns (name, price, description)
                    lines = text.split('\n')
                    current_category = None
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Detect category headers (usually all caps or title case)
                        if (line.isupper() or line.istitle()) and '$' not in line and len(line.split()) <= 3:
                            current_category = line
                        
                        # Detect menu items (contain prices)
                        elif '$' in line:
                            item = self._parse_menu_item(line, current_category)
                            if item:
                                menu_items.append(item)
                                
            except:
                continue
        
        return menu_items
    
    def _parse_menu_item(self, line: str, category: str = None) -> Dict[str, Any]:
        """
        Parse individual menu item from text line
        """
        import re
        
        # Extract price
        price_match = re.search(r'\$[\d.]+', line)
        price = price_match.group() if price_match else ""
        
        # Remove price from line to get name and description
        if price:
            line_without_price = line.replace(price, '').strip()
        else:
            line_without_price = line
        
        # Split name and description
        parts = line_without_price.split(' - ', 1)
        if len(parts) == 2:
            name, description = parts
        else:
            name = line_without_price
            description = ""
        
        return {
            "name": name.strip(),
            "price": price,
            "description": description.strip(),
            "category": category or "Main Menu"
        }
    
    def _structure_menu_data(self, menu_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Structure menu items by category
        """
        categories = {}
        
        for item in menu_items:
            category = item.get("category", "Main Menu")
            if category not in categories:
                categories[category] = []
            
            categories[category].append({
                "name": item["name"],
                "price": item["price"],
                "description": item["description"]
            })
        
        return [
            {
                "category": category,
                "items": items
            }
            for category, items in categories.items()
        ]
    
    def _generate_fallback_menu(self, restaurant_name: str) -> List[Dict[str, Any]]:
        """
        Generate a sample menu when extraction fails
        """
        return [
            {
                "category": "Starters",
                "items": [
                    {"name": "House Salad", "price": "$8", "description": "Fresh mixed greens with seasonal vegetables"},
                    {"name": "Soup of the Day", "price": "$6", "description": "Chef's daily selection"}
                ]
            },
            {
                "category": "Main Courses",
                "items": [
                    {"name": "Grilled Chicken", "price": "$18", "description": "Herb-seasoned chicken breast with vegetables"},
                    {"name": "Pan-Seared Salmon", "price": "$22", "description": "Fresh Atlantic salmon with lemon butter sauce"},
                    {"name": "Pasta Primavera", "price": "$16", "description": "Seasonal vegetables with house-made pasta"}
                ]
            },
            {
                "category": "Desserts",
                "items": [
                    {"name": "Chocolate Cake", "price": "$8", "description": "Rich chocolate layer cake"},
                    {"name": "Seasonal Fruit Tart", "price": "$7", "description": "Fresh fruit with pastry cream"}
                ]
            }
        ]