"""
Proper Agno Workflow for video generation that integrates with AgentOS
"""

from agno.workflow import Workflow, Step
from agno.db.sqlite import SqliteDb
import os
from typing import Any, Dict

def create_video_generation_workflow(
    restaurant_agent,
    menu_agent,
    content_creator_agent,
    video_producer_agent,
    db: SqliteDb
) -> Workflow:
    """
    Create the complete video generation workflow using Agno framework

    Args:
        restaurant_agent: Restaurant data extraction agent
        menu_agent: Menu analysis agent
        content_creator_agent: Content creation agent
        video_producer_agent: Video production agent
        db: Database instance for persistence

    Returns:
        Configured Agno Workflow instance
    """

    # Step 1: Restaurant Data Extraction
    restaurant_step = Step(
        name="restaurant_analysis",
        description="Extract and analyze restaurant data from Google Maps URL",
        agent=restaurant_agent,
    )

    # Step 2: Menu Analysis
    menu_step = Step(
        name="menu_analysis",
        description="Extract and analyze menu data, identify featured items",
        agent=menu_agent,
    )

    # Step 3: Content Creation
    content_step = Step(
        name="content_creation",
        description="Generate video script and promotional content",
        agent=content_creator_agent,
    )

    # Step 4: Video Production Planning
    production_step = Step(
        name="video_production",
        description="Plan video production, source assets, prepare voiceover",
        agent=video_producer_agent,
    )

    # Create the complete workflow
    workflow = Workflow(
        id="video-generation",
        name="Video Generation Workflow",
        description="Complete promotional video generation from Google Maps URL to production plan",
        db=db,
        steps=[
            restaurant_step,
            menu_step,
            content_step,
            production_step
        ],
        # Enable session state for maintaining context across steps
        session_state={
            "google_maps_url": "",
            "video_style": "casual",
            "duration": 30,
            "restaurant_data": {},
            "menu_data": {},
            "script_data": {},
            "production_plan": {}
        }
    )

    return workflow

def create_script_only_workflow(
    restaurant_agent,
    menu_agent,
    content_creator_agent,
    db: SqliteDb
) -> Workflow:
    """
    Create a faster script-only workflow for quick content generation

    Args:
        restaurant_agent: Restaurant data extraction agent
        menu_agent: Menu analysis agent
        content_creator_agent: Content creation agent
        db: Database instance

    Returns:
        Script-only Agno Workflow instance
    """

    # Streamlined steps for script generation only
    restaurant_step = Step(
        name="restaurant_analysis",
        description="Extract restaurant data from Google Maps URL",
        agent=restaurant_agent,
    )

    menu_step = Step(
        name="menu_analysis",
        description="Quick menu analysis for script context",
        agent=menu_agent,
    )

    script_step = Step(
        name="script_generation",
        description="Generate video script based on restaurant and menu data",
        agent=content_creator_agent,
    )

    workflow = Workflow(
        id="script-generation",
        name="Script Generation Workflow",
        description="Fast video script generation from Google Maps URL",
        db=db,
        steps=[
            restaurant_step,
            menu_step,
            script_step
        ],
        session_state={
            "google_maps_url": "",
            "video_style": "casual",
            "restaurant_data": {},
            "menu_data": {},
            "script_data": {}
        }
    )

    return workflow

def create_restaurant_analysis_workflow(
    restaurant_agent,
    db: SqliteDb
) -> Workflow:
    """
    Create workflow for restaurant analysis only

    Args:
        restaurant_agent: Restaurant data extraction agent
        db: Database instance

    Returns:
        Restaurant analysis Agno Workflow instance
    """

    analysis_step = Step(
        name="restaurant_analysis",
        description="Comprehensive restaurant data extraction and analysis",
        agent=restaurant_agent,
    )

    workflow = Workflow(
        id="restaurant-analysis",
        name="Restaurant Analysis Workflow",
        description="Extract and analyze restaurant data from Google Maps URL",
        db=db,
        steps=[analysis_step],
        session_state={
            "google_maps_url": "",
            "restaurant_data": {}
        }
    )

    return workflow