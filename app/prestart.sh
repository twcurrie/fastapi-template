#!/usr/bin/env bash

# Check if the application can create a connection to the database
python app/backend_pre_start.py

# Execute any database migrations
alembic upgrade head