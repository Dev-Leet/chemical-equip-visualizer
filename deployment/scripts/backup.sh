#!/bin/bash
set -e

BACKUP_DIR="$(dirname "$0")/../../backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKEND_DIR="$(dirname "$0")/../../backend"

mkdir -p "$BACKUP_DIR"

echo "Creating backup: $TIMESTAMP"

echo "Backing up database..."
cp "$BACKEND_DIR/db.sqlite3" "$BACKUP_DIR/db_$TIMESTAMP.sqlite3"

echo "Backing up media files..."
tar -czf "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" -C "$BACKEND_DIR" media/

echo "Backup complete!"
echo "Database: $BACKUP_DIR/db_$TIMESTAMP.sqlite3"
echo "Media: $BACKUP_DIR/media_$TIMESTAMP.tar.gz"
```

## backend/.dockerignore
```
__pycache__/
*.py[cod]
*$py.class
*.so
.env
venv/
env/
db.sqlite3
*.log
.git/
.gitignore
.vscode/
.idea/