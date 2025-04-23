#!/bin/bash

echo "🎶 Setting up virtual environment for Music Transcriber..."

# Exit if any command fails
set -e

# Create virtual environment
python3 -m venv venv
echo "✅ Virtual environment created."

# Activate the environment
source venv/bin/activate
echo "✅ Environment activated."

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
echo "✅ Dependencies installed."

echo "🎉 Setup complete! Run 'source venv/bin/activate' to activate your environment next time."
