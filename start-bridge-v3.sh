#!/bin/bash
# V3 Auto-Startup Script for Terminal Bridge

echo "🚀 V3 Codespace Control - Auto-Starting Terminal Bridge"
echo "======================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "📦 Installing Python3..."
    sudo apt update && sudo apt install -y python3 python3-pip
fi

# Install required packages if not available
echo "📦 Installing Python dependencies..."
pip3 install websockets asyncio --user --quiet

# Make bridge script executable
chmod +x codespace-bridge-v3.py

# Check if bridge is already running
if pgrep -f "codespace-bridge-v3.py" > /dev/null; then
    echo "⚠️  Bridge already running, stopping existing instance..."
    pkill -f "codespace-bridge-v3.py"
    sleep 2
fi

# Start bridge in background
echo "🔗 Starting V3 Terminal Bridge..."
nohup python3 codespace-bridge-v3.py --host 0.0.0.0 --port 8765 > bridge.log 2>&1 &

# Wait a moment and check if it started
sleep 3

if pgrep -f "codespace-bridge-v3.py" > /dev/null; then
    echo "✅ V3 Terminal Bridge started successfully!"
    echo "🔗 Bridge running on: ws://localhost:8765"
    echo "📝 Logs available in: bridge.log"
    echo ""
    echo "🎉 V3 AUTO-SETUP COMPLETE!"
    echo "   Your codespace is now ready for terminal access"
    echo "   Click the Terminal button in Codespace Control V3"
else
    echo "❌ Failed to start bridge, check bridge.log for errors"
fi
