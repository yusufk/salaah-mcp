#!/bin/bash
set -e

# Create a temporary build directory
echo "Creating build directory..."
mkdir -p .aws-sam/build/SalaahMCPFunction

# Install dependencies using uv
echo "Installing dependencies from pyproject.toml..."
cd ..
uv pip install --no-deps -e . --target deploy/.aws-sam/build/SalaahMCPFunction
cd deploy

# Copy application code
echo "Copying application code..."
cp -r ../app .aws-sam/build/SalaahMCPFunction/
cp -r ../run.py .aws-sam/build/SalaahMCPFunction/

echo "Build completed successfully!"
