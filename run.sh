#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "Missing .env file. Copy .env.example and fill in your token:"
    echo "  cp .env.example .env"
    exit 1
fi

if [ ! -d .venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Installing dependencies..."
.venv/bin/pip install -q -r requirements.txt

echo "Starting DJ Maurice..."
exec .venv/bin/python bot.py
