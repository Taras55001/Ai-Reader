#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
.\chat\docs\make.bat html

python manage.py collectstatic --noinput