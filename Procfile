# Procfile for deployment platforms (Render, Heroku, etc.)
# This file tells the platform how to run your application

# Web process - runs the Django application
web: gunicorn motion.wsgi:application --bind 0.0.0.0:$PORT

# Release process - runs migrations before deployment
# This runs automatically on Render before the web service starts
release: python manage.py migrate --noinput

