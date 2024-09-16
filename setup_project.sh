#!/bin/bash

# Create the project folders and set permissions
echo "Creating project folders..."
mkdir -p dags logs plugins app ml data postgres_data

# Verify the creation of the folders
if [ -d "dags" ] && [ -d "logs" ] && [ -d "plugins" ] && [ -d "app" ] && [ -d "ml" ] && [ -d "data" ] && [ -d "postgres_data" ]; then
    echo "All folders have been created successfully."
else
    echo "Error creating folders."
    exit 1
fi

# Set permissions
echo "Setting folder permissions..."
sudo chmod -R 777 dags logs plugins app ml data postgres_data

# Verify the permissions
if [ $? -eq 0 ]; then
    echo "Folder permissions set successfully."
else
    echo "Error setting folder permissions."
    exit 1
fi

# Launch Docker Compose
echo "Launching Docker Compose..."
docker compose up --build

# Verify that Docker Compose is launched successfully
if [ $? -eq 0 ]; then
    echo "Docker Compose has been launched successfully."
else
    echo "Error launching Docker Compose."
    exit 1
fi

echo "Configuration completed."
