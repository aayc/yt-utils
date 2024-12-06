#!/bin/bash

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Get python location and suggest alias
python_location=$(which python)
echo "Add this alias to your shell configuration for easy access via the yt shortcut:"
echo "alias yt='$python_location $(pwd)/run.py'"


