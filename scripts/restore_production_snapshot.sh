#!/bin/bash
# Nova Industries - 1-Click Production Snapshot Restore Script
set -e

SITE="nova.local"
BENCH_DIR="/home/naveen/frappe-bench"
BACKUP_DIR="${BENCH_DIR}/sites/${SITE}/private/backups"

echo "=== NOVA INDUSTRIES PRODUCTION RESTORE HELPER ==="
echo "Target Site: ${SITE}"

LATEST_SQL=$(ls -t ${BACKUP_DIR}/*-database.sql.gz | head -n 1)
LATEST_PUB=$(ls -t ${BACKUP_DIR}/*-files.tar | head -n 1)
LATEST_PRIV=$(ls -t ${BACKUP_DIR}/*-private-files.tar | head -n 1)

echo "Found snapshot:"
echo "  Database: ${LATEST_SQL}"
echo "  Public:   ${LATEST_PUB}"
echo "  Private:  ${LATEST_PRIV}"

cd ${BENCH_DIR}
echo "Executing bench restore..."
/home/naveen/.local/bin/bench --site ${SITE} restore "${LATEST_SQL}" \
  --with-public-files "${LATEST_PUB}" \
  --with-private-files "${LATEST_PRIV}"

echo "Clearing cache..."
/home/naveen/.local/bin/bench --site ${SITE} clear-cache

echo "=== RESTORE COMPLETED SUCCESSFULLY! ==="
