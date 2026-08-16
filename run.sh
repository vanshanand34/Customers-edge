#!/bin/bash
source ./.venv/scripts/activate

python manage.py collectstatic
uvicorn config.asgi:application
