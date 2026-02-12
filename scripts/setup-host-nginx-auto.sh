#!/bin/bash
set -e

# Automated host-level nginx setup script for motion-api
# Processes template files and sets up nginx server blocks
# Copies SSL certificates from Docker volumes to host

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then 
  echo "❌ This script must be run as root or with sudo"
  exit 1
fi

# Get domain from environment variables
MOTION_API_DOMAIN="${ALLOWED_HOSTS%% *}"
MOTION_API_DOMAIN="${MOTION_API_DOMAIN#http://}"
MOTION_API_DOMAIN="${MOTION_API_DOMAIN#https://}"
MOTION_API_DOMAIN="${MOTION_API_DOMAIN%%/*}"
MOTION_API_DOMAIN="${MOTION_API_DOMAIN%%:*}"
MOTION_API_DOMAIN="${MOTION_API_DOMAIN%% *}"

echo "🔧 Setting up host-level nginx for motion-api..."
echo "🌐 Motion API domain: $MOTION_API_DOMAIN"

# Install nginx if not already installed
if ! command -v nginx &> /dev/null; then
  echo "📦 Installing nginx..."
  apt-get update
  apt-get install -y nginx
fi

# Create directories for nginx configs
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled

# Let's Encrypt webroot (for certbot --webroot)
mkdir -p /var/www/html
chown -R www-data:www-data /var/www/html

# Update nginx.conf to include sites-enabled if not already present
if ! grep -q "include /etc/nginx/sites-enabled/\*;" /etc/nginx/nginx.conf; then
  sed -i '/^http {/a\    # Include server block configs\n    include /etc/nginx/sites-enabled/*;' /etc/nginx/nginx.conf
fi

# Increase server_names_hash_bucket_size to avoid hash bucket memory problems
if ! grep -q "server_names_hash_bucket_size" /etc/nginx/nginx.conf; then
  sed -i '/^http {/a\    server_names_hash_bucket_size 64;' /etc/nginx/nginx.conf
fi

# Get the project directory (where templates are located)
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
TEMPLATE_DIR="$PROJECT_DIR/nginx/sites-available"

# Check if template directory exists
if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "❌ Template directory not found: $TEMPLATE_DIR"
  exit 1
fi

# Check if SSL certificates exist (from Docker certbot volume)
SSL_CERTS_EXIST=false
CERTBOT_VOLUME_NAME=""
COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-motion-api}"
CERTBOT_VOLUMES=$(docker volume ls --format "{{.Name}}" | grep -E "(certbot_conf|${COMPOSE_PROJECT_NAME}.*certbot)" || true)

if [ -n "$CERTBOT_VOLUMES" ]; then
  for vol in $CERTBOT_VOLUMES; do
    if docker run --rm -v "$vol:/certs" alpine ls /certs/live/$MOTION_API_DOMAIN/fullchain.pem > /dev/null 2>&1; then
      SSL_CERTS_EXIST=true
      CERTBOT_VOLUME_NAME="$vol"
      echo "✅ SSL certificates found in Docker volume: $vol"
      break
    fi
  done
fi

# Copy certificates from Docker volume to host if they exist
if [ "$SSL_CERTS_EXIST" = true ] && [ -n "$CERTBOT_VOLUME_NAME" ]; then
  echo "📋 Copying SSL certificates from Docker volume to host..."
  mkdir -p /etc/letsencrypt/live/$MOTION_API_DOMAIN
  mkdir -p /etc/letsencrypt/archive/$MOTION_API_DOMAIN
  
  docker run --rm \
    -v "$CERTBOT_VOLUME_NAME:/source:ro" \
    -v /etc/letsencrypt:/target \
    alpine sh -c "
      if [ -f /source/live/$MOTION_API_DOMAIN/fullchain.pem ]; then
        cp -r /source/live/$MOTION_API_DOMAIN/* /target/live/$MOTION_API_DOMAIN/ 2>/dev/null || true
        cp -r /source/archive/$MOTION_API_DOMAIN/* /target/archive/$MOTION_API_DOMAIN/ 2>/dev/null || true
        echo '✅ Certificates copied to host'
      fi
    " || echo "⚠️  Could not copy certificates (may need manual setup)"
fi

# Process motion-api template
if [ -f "$TEMPLATE_DIR/motion-api" ]; then
  echo "📝 Processing motion-api server block template..."
  export ALLOWED_HOSTS_DOMAIN="$MOTION_API_DOMAIN"
  envsubst '${ALLOWED_HOSTS_DOMAIN}' < "$TEMPLATE_DIR/motion-api" > /tmp/motion-api-nginx.conf
  
  # If certificates don't exist, remove the HTTPS server block
  if [ "$SSL_CERTS_EXIST" != true ]; then
    echo "⚠️  No SSL certificates - removing HTTPS server block"
    # Remove the HTTPS server block (from "# HTTPS server" line to the closing "}")
    sed -i '/^# HTTPS server/,/^}$/d' /tmp/motion-api-nginx.conf
  else
    # Certificates exist - ensure SSL paths are correct
    sed -i "s|ssl_certificate.*|ssl_certificate /etc/letsencrypt/live/$MOTION_API_DOMAIN/fullchain.pem;|g" /tmp/motion-api-nginx.conf
    sed -i "s|ssl_certificate_key.*|ssl_certificate_key /etc/letsencrypt/live/$MOTION_API_DOMAIN/privkey.pem;|g" /tmp/motion-api-nginx.conf
  fi
  
  mv /tmp/motion-api-nginx.conf /etc/nginx/sites-available/motion-api
  ln -sf /etc/nginx/sites-available/motion-api /etc/nginx/sites-enabled/motion-api
  echo "✅ Created and enabled motion-api server block"
else
  echo "❌ Template file not found: $TEMPLATE_DIR/motion-api"
  exit 1
fi

# Test nginx configuration
echo "🧪 Testing nginx configuration..."
if nginx -t; then
  echo "✅ Nginx configuration is valid"
  systemctl reload nginx || systemctl restart nginx
  echo "✅ Nginx reloaded successfully"
else
  echo "❌ Nginx configuration test failed!"
  exit 1
fi

echo "✅ Host-level nginx setup completed!"
