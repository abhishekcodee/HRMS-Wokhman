#!/bin/bash
set -e

SITE_NAME=${1:-"hrms.local"}
ADMIN_PASSWORD=${2:-"AdminPass123!"}
DB_ROOT_PASSWORD=${3:-"YourSecureRootPassword123!"}

echo "=========================================================="
echo " Bootstrapping Sovereign Frappe HRMS Site: $SITE_NAME"
echo "=========================================================="

cd /home/frappe/frappe-bench

# Verify database connection
echo "Checking MariaDB connectivity..."
mysqladmin ping -h mariadb -u root -p"$DB_ROOT_PASSWORD" --silent

# Check if using an external existing database
if [ -n "$DB_HOST" ] && [ -n "$DB_NAME" ] && [ -n "$DB_PASSWORD" ]; then
    echo "Connecting to custom database: $DB_NAME on $DB_HOST:$DB_PORT..."
    python3 /home/frappe/frappe-bench/apps/hrms/docker/generate_site_config.py "$SITE_NAME" "/home/frappe/frappe-bench/sites"
    bench --site "$SITE_NAME" migrate
    bench --site "$SITE_NAME" install-app erpnext || true
    bench --site "$SITE_NAME" install-app hrms || true
    bench --site "$SITE_NAME" clear-cache
elif [ ! -d "sites/$SITE_NAME" ]; then
    echo "Creating site $SITE_NAME on self-hosted database..."
    bench new-site "$SITE_NAME" \
        --mariadb-root-password "$DB_ROOT_PASSWORD" \
        --admin-password "$ADMIN_PASSWORD" \
        --no-mariadb-socket

    echo "Configuring independent production parameters..."
    bench --site "$SITE_NAME" set-config developer_mode 0
    bench --site "$SITE_NAME" set-config enable_telemetry 0
    bench --site "$SITE_NAME" set-config telemetry 0
    bench --site "$SITE_NAME" set-config push_relay_server_url ""

    echo "Installing applications: erpnext and hrms..."
    bench --site "$SITE_NAME" install-app erpnext
    bench --site "$SITE_NAME" install-app hrms

    echo "Enabling scheduler..."
    bench --site "$SITE_NAME" enable-scheduler

    echo "Setting default site..."
    bench use "$SITE_NAME"

    echo "Running migration and clearing cache..."
    bench --site "$SITE_NAME" migrate
    bench --site "$SITE_NAME" clear-cache
else
    echo "Site $SITE_NAME already exists. Running migration..."
    bench --site "$SITE_NAME" migrate
    bench --site "$SITE_NAME" clear-cache
fi

echo "=========================================================="
echo " Sovereign site $SITE_NAME is ready!"
echo " Admin User: Administrator"
echo " Access URL: http://localhost (or configured domain)"
echo "=========================================================="
