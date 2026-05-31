#!/bin/bash
# LED Pixelstick Code Deployment Script
# Automatically copies code.py to the Plasma 2040 microcontroller

MICROCONTROLLER_PATH="/media/gregor/CIRCUITPY"
SOURCE_FILE="code.py"
TARGET_FILE="$MICROCONTROLLER_PATH/code.py"

echo "🚀 Deploying LED Pixelstick code to Plasma 2040..."

# Check if microcontroller is mounted
if [ ! -d "$MICROCONTROLLER_PATH" ]; then
    echo "❌ Error: Plasma 2040 not found at $MICROCONTROLLER_PATH"
    echo "   Make sure your microcontroller is connected and mounted"
    exit 1
fi

# Check if source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "❌ Error: Source file $SOURCE_FILE not found"
    exit 1
fi

# Copy the file
echo "📁 Copying $SOURCE_FILE to microcontroller..."
cp "$SOURCE_FILE" "$TARGET_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "📊 File info:"
    ls -l "$TARGET_FILE"
    echo "🔄 CircuitPython will auto-restart with new code"
else
    echo "❌ Deployment failed!"
    exit 1
fi