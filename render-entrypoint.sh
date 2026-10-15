#!/bin/bash
set -e

PORT=${PORT:-10000}
SITE=${SITE_NAME:-nova.local}

echo "=== STARTING NOVA INDUSTRIES ERPNEXT ON RENDER ==="
echo "Port: ${PORT}"
echo "Site: ${SITE}"

# Start Redis
redis-server --port 11000 --daemonize yes
redis-server --port 13000 --daemonize yes

# Start MariaDB service if installed locally
if command -v service &> /dev/null; then
    service mariadb start || true
elif command -v mysqld &> /dev/null; then
    mysqld_safe &
fi

cd /home/naveen/frappe-bench

# If site does not exist, restore from backup bundle
if [ ! -d "sites/${SITE}" ]; then
    echo "Restoring ${SITE} from production snapshot..."
    bench --site ${SITE} restore /home/naveen/frappe-bench/sites/nova.local/private/backups/*-database.sql.gz \
      --with-public-files /home/naveen/frappe-bench/sites/nova.local/private/backups/*-files.tar \
      --with-private-files /home/naveen/frappe-bench/sites/nova.local/private/backups/*-private-files.tar || true
fi

echo "Clearing cache..."
bench --site ${SITE} clear-cache || true

echo "Starting ERPNext Web Service on port ${PORT}..."
exec bench serve --port ${PORT}
