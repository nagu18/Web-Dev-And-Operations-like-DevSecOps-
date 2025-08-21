#!/bin/bash
sleep 20 && python3 manage.py migrate && python3 manage.py createsu && gunicorn code_chat.wsgi:application --bind 0.0.0.0:8000