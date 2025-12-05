# Deployment Guide

## 📋 Step-by-Step: Deploying to Render (Example)

### Prerequisites
1. Git repository (GitHub, GitLab, etc.)
2. Render account (free at render.com)

### Step 1: Prepare Your Project

#### 1.1 Update `requirements.txt`
Make sure it includes production dependencies:
```txt
Django==6.0
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
drf-yasg==1.21.11
psycopg2-binary==2.9.9  # PostgreSQL adapter
gunicorn==21.2.0  # WSGI server
whitenoise==6.6.0  # Static file serving
python-decouple==3.8  # Environment variables
```

#### 1.2 Create `runtime.txt` (optional)
```txt
python-3.13.0
```

#### 1.3 Create `Procfile`
```txt
web: gunicorn recipe_cookbok_management.wsgi:application
release: python manage.py migrate
```

#### 1.4 Update `settings.py` for Production

Create `recipe_cookbok_management/settings.py` with environment-based configuration:

```python
import os
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='dev-key-change-in-production')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database - Use PostgreSQL in production
if config('DATABASE_URL', default=None):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=config('DATABASE_URL'))
    }
else:
    # Development: SQLite3
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ... rest of your settings ...
```

#### 1.5 Add `whitenoise` middleware
In `settings.py`, add WhiteNoise to middleware (before CommonMiddleware):
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... rest
]
```

### Step 2: Set Up PostgreSQL Database on Render

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Choose:
   - Name: `recipe-cookbook-db`
   - Database: `recipe_cookbook`
   - User: `recipe_user`
   - Region: Choose closest
   - Plan: Free (for testing)
4. Click "Create Database"
5. **Save the connection string** (you'll need it)

### Step 3: Deploy Django Application

1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect your Git repository
4. Configure:
   - **Name**: `recipe-cookbook-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn recipe_cookbok_management.wsgi:application`
   - **Plan**: Free (for testing)

### Step 4: Configure Environment Variables

In Render dashboard, add these environment variables:

```
SECRET_KEY=your-super-secret-key-here-generate-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://user:password@host:port/dbname  # From PostgreSQL service
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Deploy and Migrate

1. Click "Create Web Service"
2. Render will:
   - Build your app
   - Run migrations automatically (via Procfile release command)
   - Start the server

### Step 6: Create Superuser

After deployment, create a superuser via Render shell:
1. Go to your service → "Shell"
2. Run:
```bash
python manage.py createsuperuser
```

## 🔄 Migrating from SQLite3 to PostgreSQL

### Option 1: Using Django's dumpdata/loaddata

```bash
# 1. Export data from SQLite3
python manage.py dumpdata > data.json

# 2. Update settings.py to use PostgreSQL
# 3. Run migrations on PostgreSQL
python manage.py migrate

# 4. Load data into PostgreSQL
python manage.py loaddata data.json
```

### Option 2: Using pgloader (Advanced)

```bash
# Install pgloader
brew install pgloader  # macOS
# or apt-get install pgloader  # Linux

# Convert SQLite to PostgreSQL
pgloader db.sqlite3 postgresql://user:pass@host/dbname
```

## 📝 Alternative: Railway Deployment

### Quick Setup:

1. **Install Railway CLI:**
```bash
npm i -g @railway/cli
railway login --browserless
```

2. **Initialize project:**
```bash
railway init
railway add  # Add PostgreSQL database
```

3. **Deploy:**
```bash
railway up
```

4. **Set environment variables:**
```bash
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
```

5. **Run migrations:**
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

## 🔒 Production Checklist

Before going live:

- [ ] Change `SECRET_KEY` (use environment variable)
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure static files (WhiteNoise or CDN)
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS (if needed for frontend)
- [ ] Set up logging
- [ ] Configure email backend (if needed)
- [ ] Set up monitoring/error tracking
- [ ] Backup strategy for database
- [ ] Set up CI/CD pipeline


## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Render Django Guide](https://render.com/docs/deploy-django)
- [Railway Django Guide](https://docs.railway.app/guides/django)
- [PostgreSQL with Django](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)

## 🆘 Common Issues

### Issue: Static files not loading
**Solution:** Add WhiteNoise and configure `STATIC_ROOT`

### Issue: Database connection errors
**Solution:** Check `DATABASE_URL` format and credentials

### Issue: 500 errors in production
**Solution:** Check logs, ensure `DEBUG=False`, verify `ALLOWED_HOSTS`

### Issue: Migrations not running
**Solution:** Add `release` command in Procfile or run manually

## 💡 Quick Start Commands

```bash
# Install production dependencies
pip install psycopg2-binary gunicorn whitenoise python-decouple dj-database-url

# Update requirements.txt
pip freeze > requirements.txt

# Test locally with production settings
python manage.py check --deploy
```

