#!/bin/bash
set -e

# Create a temporary build directory
echo "Creating build directory..."
mkdir -p .aws-sam/build

# Install dependencies using uv
echo "Installing dependencies from pyproject.toml..."
cd ..
uv pip install --no-deps -e . --target deploy/.aws-sam/build
cd deploy

# Copy application code
echo "Copying application code..."
cp -r ../app .aws-sam/build/
cp -r ../run.py .aws-sam/build/

# Create deployment package
echo "Creating deployment package..."
cd .aws-sam/build
zip -r ../../deployment.zip .
cd ../..

echo "Build completed successfully!"
