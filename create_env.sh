#!/bin/sh
echo "Copying .env.example to .env"
cp .env.example .env

echo "Making create_env.sh executable"
chmod +x create_env.sh

echo "Script executed successfully"