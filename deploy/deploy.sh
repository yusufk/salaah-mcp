#!/bin/bash
set -e

# Build the application
echo "Building the application..."
./build.sh

# Deploy with SAM
echo "Deploying with SAM to Ireland (eu-west-1)..."
sam deploy \
  --template-file template.yaml \
  --stack-name salaah-mcp \
  --region eu-west-1 \
  --capabilities CAPABILITY_IAM \
  --resolve-s3

echo "Deployment completed successfully!"
