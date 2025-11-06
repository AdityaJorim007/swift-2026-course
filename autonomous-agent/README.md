# Autonomous Swift Course Content Agent

> **Self-perpetuating content generation system that keeps your Swift course cutting-edge**

## 🤖 What It Does

This autonomous agent continuously:
- **Scrapes** latest Swift/iOS content from multiple sources
- **Analyzes** trends and extracts actionable insights
- **Generates** new course chapters and updates
- **Deploys** changes automatically to your course

## 🎯 Content Sources

### YouTube Channels
- Apple Developer
- Sean Allen
- Stewart Lynch
- CodeWithChris
- Kavsoft

### Documentation & Blogs
- Apple Developer Documentation
- Swift.org Blog
- GitHub Trending Swift repos

### Community
- r/iOSProgramming
- r/swift
- Developer discussions

## 🚀 Quick Deployment

### 1. Set Environment Variables
```bash
export OPENAI_API_KEY="your-openai-key"
export GITHUB_TOKEN="your-github-token"
```

### 2. Deploy Locally
```bash
cd autonomous-agent
pip install -r requirements.txt
python content_agent.py
```

### 3. Deploy to Cloud (Docker)
```bash
./deploy.sh
```

### 4. GitHub Actions (Automated)
The agent runs automatically every 6 hours via GitHub Actions.

## 🔧 Configuration

Edit `config.py` to customize:
- Content sources and channels
- Generation frequency
- Quality thresholds
- Content keywords

## 📊 What Gets Generated

### New Chapters
- Performance optimization techniques
- Latest API usage patterns
- Monetization strategies
- Architecture improvements

### Code Updates
- Latest Swift syntax
- New framework integrations
- Performance benchmarks
- Real-world examples

### Insights
- Trending developer topics
- Popular libraries and tools
- Community pain points
- Emerging best practices

## 🎛️ Monitoring

### Check Agent Status
```bash
./monitor_agent.sh
```

### View Logs
```bash
docker logs -f swift-course-agent
```

### Manual Trigger
```bash
# Trigger single content generation cycle
python content_agent.py --single-run
```

## 🔄 How It Works

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Scrape        │───▶│   Analyze        │───▶│   Generate      │
│   - YouTube     │    │   - Extract      │    │   - New chapters│
│   - GitHub      │    │   - Insights     │    │   - Code updates│
│   - Apple Docs  │    │   - Trends       │    │   - Examples    │
│   - Reddit      │    │   - Pain points  │    │   - Strategies  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                    ┌─────────────────────────┐
                    │      Deploy             │
                    │   - Update repo         │
                    │   - Build course        │
                    │   - GitHub Pages        │
                    └─────────────────────────┘
```

## 🎯 Business Impact

### Automatic Competitive Advantage
- Always includes latest Swift features
- Covers trending topics before competitors
- Incorporates community insights
- Updates performance benchmarks

### Content Quality
- AI-powered analysis ensures relevance
- Production-focused examples
- Real performance metrics
- Business impact data

### Time Savings
- No manual content research
- Automated course updates
- Continuous deployment
- Self-maintaining system

## 🛡️ Security & Privacy

- No sensitive data stored
- API keys via environment variables
- Read-only access to public content
- Respects rate limits and ToS

## 📈 Metrics & Analytics

The agent tracks:
- Content generation frequency
- Source reliability scores
- Generated content quality
- Course engagement metrics

## 🔧 Troubleshooting

### Agent Not Running
```bash
docker restart swift-course-agent
```

### API Rate Limits
- Adjust `CYCLE_INTERVAL_HOURS` in config
- Implement exponential backoff
- Use multiple API keys

### Content Quality Issues
- Adjust quality thresholds in config
- Update generation prompts
- Review source reliability

## 🚀 Advanced Features

### Custom Content Sources
Add new sources in `config.py`:
```python
CUSTOM_SOURCES = [
    'https://your-blog.com/feed.xml',
    'https://api.custom-source.com/swift'
]
```

### Content Filtering
Customize keyword filtering:
```python
CONTENT_KEYWORDS = [
    'your-specific-topics',
    'niche-frameworks'
]
```

### Generation Customization
Modify AI prompts for specific focus areas:
```python
CUSTOM_PROMPT = """
Focus on enterprise iOS development...
"""
```

---

**The agent runs 24/7, ensuring your Swift course stays ahead of the curve automatically.**
