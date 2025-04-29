#!/bin/bash
echo "Ensuring dependencies for Main Bot are up to date..."
# This command installs/updates/removes packages to match requirements.txt
uv pip sync requirements.txt

# Check if the sync command was successful before running the bot
if [ $? -ne 0 ]; then
  echo "Error syncing dependencies. Exiting."
  exit 1
fi

echo "Starting Dummies..."
uv run python dummies.py # Use the renamed file if you did