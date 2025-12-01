#!/bin/bash
# Run the React frontend application
echo "Starting React frontend server..."
cd "$(dirname "$0")"
if [ -d "node_modules" ]; then
    exec npm run dev
else
    exec npx npm install
    exec npm run dev
fi