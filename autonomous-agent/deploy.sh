#!/bin/bash

# Autonomous Content Agent Deployment Script
# Deploys the agent to run continuously on a cloud server

set -e

echo "🚀 Deploying Autonomous Content Generation Agent..."

# Check required environment variables
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY environment variable is required"
    exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN environment variable is required"
    exit 1
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t swift-course-agent .

# Stop existing container if running
echo "🛑 Stopping existing agent..."
docker stop swift-course-agent 2>/dev/null || true
docker rm swift-course-agent 2>/dev/null || true

# Run new container
echo "▶️ Starting autonomous agent..."
docker run -d \
    --name swift-course-agent \
    --restart unless-stopped \
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \
    -e GITHUB_TOKEN="$GITHUB_TOKEN" \
    -v $(pwd)/logs:/app/logs \
    swift-course-agent

echo "✅ Autonomous agent deployed successfully!"
echo "📊 Monitor logs with: docker logs -f swift-course-agent"
echo "🔍 Check status with: docker ps | grep swift-course-agent"

# Create monitoring script
cat > monitor_agent.sh << 'EOF'
#!/bin/bash
# Monitor the autonomous agent

echo "📊 Swift Course Agent Status"
echo "=========================="

# Check if container is running
if docker ps | grep -q swift-course-agent; then
    echo "✅ Agent is running"
    
    # Show recent logs
    echo ""
    echo "📝 Recent logs:"
    docker logs --tail 20 swift-course-agent
    
    # Show resource usage
    echo ""
    echo "💾 Resource usage:"
    docker stats swift-course-agent --no-stream
else
    echo "❌ Agent is not running"
    echo "🔄 Attempting to restart..."
    docker start swift-course-agent
fi
EOF

chmod +x monitor_agent.sh

echo "🎯 Agent is now running autonomously!"
echo "   - Scrapes content every 6 hours"
echo "   - Generates new course material automatically"
echo "   - Updates GitHub repository"
echo "   - Deploys changes to GitHub Pages"
echo ""
echo "📋 Management commands:"
echo "   ./monitor_agent.sh     - Check status and logs"
echo "   docker logs -f swift-course-agent  - Follow logs"
echo "   docker restart swift-course-agent  - Restart agent"
