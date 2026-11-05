#!/bin/bash

# Spotify to Apple Music Migration Tool - Setup Script

echo "🎵 Setting up Spotify to Apple Music Migration Tool..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ ! -d "venv" ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium

echo ""
echo "================================"
echo "✅ Setup complete!"
echo "================================"
echo ""
echo "To run the tool:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "To deactivate when done:"
echo "  deactivate"
echo ""
