#!/bin/sh

# setup log folder
mkdir -p logs/

# build js client
cd frontend/app
npm install 
npm run build

# back to the parent directory
cd ../..

# enable your virtual environment first for this line
cd backend
python fixtures.py
