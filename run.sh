#!/bin/bash

set -e

# Create and activate a virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install required Python libraries
pip install --upgrade pip
pip install pillow

# Run the main Python script
python main.py

# Deactivate the virtual environment
deactivate
