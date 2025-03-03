#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y graphviz graphviz-dev

# Install Python dependencies
pip install -r requirements.txt
