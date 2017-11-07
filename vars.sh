#!/usr/bin/env bash

export FLASK_APP=app.py
export DATABASE_URL="postgresql://postgres:carleybaer@localhost:5432/commit"
export APP_SETTINGS=config.DevelopmentConfig
