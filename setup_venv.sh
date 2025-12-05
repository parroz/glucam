#!/bin/bash
# Setup script for Raspberry Pi Camera project
# Creates virtual environment and installs dependencies

echo "Setting up virtual environment..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Virtual environment setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "Then you can run the script with:"
echo "  python camera_viewer.py"
echo ""
echo "To deactivate, run:"
echo "  deactivate"

