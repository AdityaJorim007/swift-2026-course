#!/usr/bin/env python3
"""
Autonomous Swift Course Content Generation Agent
Scrapes latest Swift/iOS content and generates course updates
"""

import asyncio
import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
import aiohttp
import feedparser
from bs4 import BeautifulSoup
import openai
from github import Github
import subprocess

class ContentAgent:
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.repo = self.github.get_repo('durellwilson/swift-2026-course')
        
        # Content sources
        self.sources = {
            'apple_docs': 'https://developer.apple.com/documentation/updates/',
            'swift_blog': 'https://swift.org/blog/',
            'wwdc_videos': 'https://developer.apple.com/videos/',
            'youtube_channels': [
                'UC2D6eRvCeMtcF5OGHf1-trw',  # Apple Developer
                'UCuP2vJ6kRutQBfRmdcI92mA',  # Sean Allen
                'UC_7ZKZSqtXAcbmhEzVyg8Pw',  # Stewart Lynch
            ],
            'github_trending': 'https://github.com/trending/swift',
            'reddit_feeds': ['r/iOSProgramming', 'r/swift']
        }
        
    async def run_autonomous_cycle(self):
        """Main autonomous cycle - runs continuously"""
        while True:
            try:
                print(f"🤖 Starting content cycle at {datetime.now()}")
                
                # 1. Scrape latest content
                content_data = await self.scrape_all_sources()
                
                # 2. Analyze and generate insights
                insights = await self.analyze_content(content_data)
                
                # 3. Generate new course content
                new_content = await self.generate_course_updates(insights)
                
                # 4. Update course repository
                await self.update_course_repo(new_content)
                
                # 5. Deploy updates
                await self.deploy_updates()
                
                print(f"✅ Cycle completed. Sleeping for 6 hours...")
                await asyncio.sleep(6 * 3600)  # Run every 6 hours
                
            except Exception as e:
                print(f"❌ Error in autonomous cycle: {e}")
                await asyncio.sleep(1800)  # Wait 30 minutes on error

    async def scrape_all_sources(self) -> Dict[str, Any]:
        """Scrape content from all configured sources"""
        content = {}
        
        async with aiohttp.ClientSession() as session:
            # Apple Developer Updates
            content['apple_updates'] = await self.scrape_apple_docs(session)
            
            # YouTube content
            content['youtube_videos'] = await self.scrape_youtube_content(session)
            
            # GitHub trending
            content['github_trending'] = await self.scrape_github_trending(session)
            
            # Swift blog
            content['swift_blog'] = await self.scrape_swift_blog(session)
            
            # Reddit discussions
            content['reddit_discussions'] = await self.scrape_reddit_content(session)
            
        return content

    async def scrape_youtube_content(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Scrape latest YouTube videos from Swift/iOS channels"""
        videos = []
        
        for channel_id in self.sources['youtube_channels']:
            try:
                # Use YouTube RSS feed (no API key required)
                feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
                async with session.get(feed_url) as response:
                    feed_data = await response.text()
                    
                feed = feedparser.parse(feed_data)
                
                for entry in feed.entries[:5]:  # Latest 5 videos per channel
                    # Only include recent videos (last 7 days)
                    pub_date = datetime(*entry.published_parsed[:6])
                    if datetime.now() - pub_date <= timedelta(days=7):
                        videos.append({
                            'title': entry.title,
                            'url': entry.link,
                            'published': pub_date.isoformat(),
                            'description': entry.summary,
                            'channel': entry.author
                        })
                        
            except Exception as e:
                print(f"Error scraping YouTube channel {channel_id}: {e}")
                
        return videos

    async def scrape_apple_docs(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Scrape Apple Developer documentation updates"""
        updates = []
        
        try:
            async with session.get(self.sources['apple_docs']) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find documentation updates
                update_items = soup.find_all('div', class_='update-item')[:10]
                
                for item in update_items:
                    title_elem = item.find('h3')
                    date_elem = item.find('time')
                    desc_elem = item.find('p')
                    
                    if title_elem and date_elem:
                        updates.append({
                            'title': title_elem.get_text().strip(),
                            'date': date_elem.get('datetime'),
                            'description': desc_elem.get_text().strip() if desc_elem else '',
                            'url': item.find('a')['href'] if item.find('a') else ''
                        })
                        
        except Exception as e:
            print(f"Error scraping Apple docs: {e}")
            
        return updates

    async def scrape_github_trending(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Scrape GitHub trending Swift repositories"""
        repos = []
        
        try:
            async with session.get(self.sources['github_trending']) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                repo_items = soup.find_all('article', class_='Box-row')[:10]
                
                for item in repo_items:
                    title_elem = item.find('h2')
                    desc_elem = item.find('p')
                    stars_elem = item.find('a', href=re.compile(r'/stargazers'))
                    
                    if title_elem:
                        repo_name = title_elem.get_text().strip().replace('\n', '').replace(' ', '')
                        repos.append({
                            'name': repo_name,
                            'description': desc_elem.get_text().strip() if desc_elem else '',
                            'stars': stars_elem.get_text().strip() if stars_elem else '0',
                            'url': f"https://github.com/{repo_name}"
                        })
                        
        except Exception as e:
            print(f"Error scraping GitHub trending: {e}")
            
        return repos

    async def scrape_swift_blog(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Scrape Swift.org blog posts"""
        posts = []
        
        try:
            feed_url = "https://swift.org/blog/feed.xml"
            async with session.get(feed_url) as response:
                feed_data = await response.text()
                
            feed = feedparser.parse(feed_data)
            
            for entry in feed.entries[:5]:
                pub_date = datetime(*entry.published_parsed[:6])
                if datetime.now() - pub_date <= timedelta(days=30):  # Last 30 days
                    posts.append({
                        'title': entry.title,
                        'url': entry.link,
                        'published': pub_date.isoformat(),
                        'summary': entry.summary
                    })
                    
        except Exception as e:
            print(f"Error scraping Swift blog: {e}")
            
        return posts

    async def scrape_reddit_content(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Scrape Reddit discussions from iOS/Swift subreddits"""
        discussions = []
        
        for subreddit in self.sources['reddit_feeds']:
            try:
                url = f"https://www.reddit.com/{subreddit}/hot.json?limit=10"
                headers = {'User-Agent': 'SwiftCourseBot/1.0'}
                
                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                    
                for post in data['data']['children']:
                    post_data = post['data']
                    
                    # Filter for relevant content
                    if any(keyword in post_data['title'].lower() for keyword in 
                          ['swift', 'ios', 'xcode', 'swiftui', 'performance', 'monetization']):
                        discussions.append({
                            'title': post_data['title'],
                            'url': f"https://reddit.com{post_data['permalink']}",
                            'score': post_data['score'],
                            'comments': post_data['num_comments'],
                            'subreddit': subreddit
                        })
                        
            except Exception as e:
                print(f"Error scraping Reddit {subreddit}: {e}")
                
        return discussions

    async def analyze_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze scraped content using AI to extract insights"""
        
        analysis_prompt = f"""
        Analyze this Swift/iOS development content and extract key insights for course updates:

        YouTube Videos: {json.dumps(content_data.get('youtube_videos', [])[:5], indent=2)}
        Apple Updates: {json.dumps(content_data.get('apple_updates', [])[:5], indent=2)}
        GitHub Trending: {json.dumps(content_data.get('github_trending', [])[:5], indent=2)}
        Swift Blog: {json.dumps(content_data.get('swift_blog', [])[:3], indent=2)}
        Reddit Discussions: {json.dumps(content_data.get('reddit_discussions', [])[:5], indent=2)}

        Extract:
        1. New Swift/iOS features or APIs to cover
        2. Performance optimization techniques mentioned
        3. Monetization strategies discussed
        4. Popular libraries or tools trending
        5. Common developer pain points
        6. Emerging best practices

        Return JSON with structured insights.
        """

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3
            )
            
            insights = json.loads(response.choices[0].message.content)
            return insights
            
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return {}

    async def generate_course_updates(self, insights: Dict[str, Any]) -> Dict[str, str]:
        """Generate new course content based on insights"""
        
        generation_prompt = f"""
        Based on these insights from the Swift/iOS community, generate new course content:

        {json.dumps(insights, indent=2)}

        Generate:
        1. One new chapter/lesson (markdown format)
        2. Updated code examples using latest APIs
        3. New performance optimization techniques
        4. Updated monetization strategies

        Focus on production-ready, business-focused content that gives developers a competitive edge.
        Include real code examples and measurable outcomes.

        Return JSON with:
        - "new_chapter": markdown content for new chapter
        - "code_updates": updated code examples
        - "performance_tips": new optimization techniques
        - "monetization_updates": new revenue strategies
        """

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": generation_prompt}],
                temperature=0.4,
                max_tokens=4000
            )
            
            updates = json.loads(response.choices[0].message.content)
            return updates
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return {}

    async def update_course_repo(self, new_content: Dict[str, str]):
        """Update the course repository with new content"""
        
        if not new_content:
            return
            
        try:
            # Create new chapter file
            if 'new_chapter' in new_content:
                timestamp = datetime.now().strftime("%Y%m%d")
                filename = f"book/src/auto-generated/chapter_{timestamp}.md"
                
                # Create file content
                file_content = new_content['new_chapter']
                
                # Create or update file in repo
                try:
                    file = self.repo.get_contents(filename)
                    self.repo.update_file(
                        filename,
                        f"Auto-update: New chapter {timestamp}",
                        file_content,
                        file.sha
                    )
                except:
                    # File doesn't exist, create it
                    self.repo.create_file(
                        filename,
                        f"Auto-generate: New chapter {timestamp}",
                        file_content
                    )
                    
            # Update SUMMARY.md to include new chapter
            if 'new_chapter' in new_content:
                await self.update_summary_file(timestamp)
                
            print(f"✅ Repository updated with new content")
            
        except Exception as e:
            print(f"Error updating repository: {e}")

    async def update_summary_file(self, timestamp: str):
        """Update SUMMARY.md to include new auto-generated content"""
        
        try:
            summary_file = self.repo.get_contents("book/src/SUMMARY.md")
            current_content = summary_file.decoded_content.decode('utf-8')
            
            # Add new chapter to auto-generated section
            new_line = f"- [Auto-Generated {timestamp}](./auto-generated/chapter_{timestamp}.md)\n"
            
            if "# Auto-Generated Content" not in current_content:
                current_content += "\n# Auto-Generated Content\n\n"
                
            current_content += new_line
            
            self.repo.update_file(
                "book/src/SUMMARY.md",
                f"Auto-update: Add chapter {timestamp} to summary",
                current_content,
                summary_file.sha
            )
            
        except Exception as e:
            print(f"Error updating SUMMARY.md: {e}")

    async def deploy_updates(self):
        """Deploy course updates using GitHub Actions"""
        
        try:
            # Trigger GitHub Actions workflow
            workflow = self.repo.get_workflow("deploy.yml")
            workflow.create_dispatch("main")
            
            print("✅ Deployment triggered")
            
        except Exception as e:
            print(f"Error triggering deployment: {e}")

# Deployment script
if __name__ == "__main__":
    agent = ContentAgent()
    asyncio.run(agent.run_autonomous_cycle())
