#!/usr/bin/env bash

export FLASK_APP=app.py
export DATABASE_URL="postgresql://localhost/commit"
export APP_SETTINGS=config.DevelopmentConfig
