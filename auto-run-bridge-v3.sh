#!/bin/bash
# V3 Auto-Run Script - Executes automatically when files sync

echo "🔄 V3 Auto-Run: Setting up terminal bridge..."

# Wait for files to be available
while [ ! -f "codespace-bridge-v3.py" ] || [ ! -f "start-bridge-v3.sh" ]; do
    echo "⏳ Waiting for V3 files to sync..."
    sleep 5
done

# Make scripts executable
chmod +x codespace-bridge-v3.py
chmod +x start-bridge-v3.sh

# Run the startup script
echo "🚀 Running V3 startup script..."
./start-bridge-v3.sh

echo "✅ V3 Auto-Run complete!"
