#!/bin/bash
source venv/bin/activate
flask db init
flask db migrate
flask db upgrade
flask translate compile
exec gunicorn -w 4 --bind 0.0.0.0:5000 wsgi:app
