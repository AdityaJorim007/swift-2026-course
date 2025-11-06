"""
Configuration for the autonomous content generation agent
"""

import os
from typing import Dict, List

class AgentConfig:
    # API Keys (set via environment variables)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    # Repository settings
    REPO_OWNER = 'durellwilson'
    REPO_NAME = 'swift-2026-course'
    
    # Content sources configuration
    YOUTUBE_CHANNELS = [
        'UC2D6eRvCeMtcF5OGHf1-trw',  # Apple Developer
        'UCuP2vJ6kRutQBfRmdcI92mA',  # Sean Allen
        'UC_7ZKZSqtXAcbmhEzVyg8Pw',  # Stewart Lynch
        'UCDIBBmkZIB2hjBsk5hqk9rQ',  # CodeWithChris
        'UC2Xd-TjJByJyK2w1zNwY0zQ',  # Kavsoft
    ]
    
    CONTENT_KEYWORDS = [
        'swift', 'ios', 'xcode', 'swiftui', 'performance', 
        'monetization', 'app store', 'optimization', 'concurrency',
        'core ml', 'widgetkit', 'app intents', 'swiftdata'
    ]
    
    # Generation settings
    CYCLE_INTERVAL_HOURS = 6
    MAX_VIDEOS_PER_CHANNEL = 5
    MAX_GITHUB_REPOS = 10
    CONTENT_FRESHNESS_DAYS = 7
    
    # Quality thresholds
    MIN_VIDEO_VIEWS = 1000
    MIN_GITHUB_STARS = 50
    MIN_REDDIT_SCORE = 10
    
    # Content generation prompts
    ANALYSIS_PROMPT_TEMPLATE = """
    Analyze this Swift/iOS development content and extract actionable insights:
    
    {content_summary}
    
    Focus on:
    1. New APIs or language features
    2. Performance optimization techniques
    3. Monetization strategies and conversion tactics
    4. Architecture patterns for scale
    5. Developer productivity improvements
    6. App Store optimization techniques
    
    Return structured JSON with specific, actionable insights.
    """
    
    GENERATION_PROMPT_TEMPLATE = """
    Generate production-focused Swift course content based on these insights:
    
    {insights}
    
    Create content that:
    - Provides competitive advantage to developers
    - Includes real performance metrics and business impact
    - Contains working code examples
    - Focuses on monetization and user retention
    - Addresses current developer pain points
    
    Generate:
    1. New chapter with practical examples
    2. Updated code patterns using latest APIs
    3. Performance optimization techniques with benchmarks
    4. Monetization strategies with conversion data
    
    Format as production-ready markdown with code blocks.
    """
