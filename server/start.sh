#!/bin/bash

# Install Git LFS
apt-get update && apt-get install -y git-lfs
git lfs install
git lfs pull

# Now run your server
uvicorn main:app --host 0.0.0.0 --port 8000
