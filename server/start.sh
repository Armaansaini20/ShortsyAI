#!/bin/bash

echo "🔄 Pulling Git LFS files..."
git lfs install
git lfs pull

echo "🚀 Starting backend..."
uvicorn main:app --host 0.0.0.0 --port 8000
