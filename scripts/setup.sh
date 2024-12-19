#!/bin/bash
echo ##active_line2##

echo ##active_line3##
# Create and activate a virtual environment
echo ##active_line4##
python3 -m venv venv
echo ##active_line5##
source /Users/crashair/AI-Software/_Interpreter/Projects/Project-001/venv/bin/activate
echo ##active_line6##

echo ##active_line7##
# Install project dependencies
echo ##active_line8##
pip install -r requirements.txt
echo ##active_line9##

echo ##active_line10##
# Run the project profile script
echo ##active_line11##
interpreter --profile /Users/crashair/AI-Software/_Interpreter/Projects/Project-001/project-001-profile.py
