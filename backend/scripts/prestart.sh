#! /usr/bin/env bash

# Run migrations
alembic upgrade head

# Create initial data in DB
python initial_data.py