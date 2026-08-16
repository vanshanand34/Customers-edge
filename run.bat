@echo off
call .venv/scripts/activate

python manage.py collectstatic
uvicorn config.asgi:application
