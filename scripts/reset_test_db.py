#!/usr/bin/env python3
"""
Reset test JSON database files by backing up existing files and writing empty lists.
Usage: python scripts/reset_test_db.py [--no-backup] [--yes]

This script creates a timestamped backup directory in repo root `backups/` and copies
existing JSON files into it before clearing the active files by writing an empty list.

Files cleared:
- approved_confessions.json
- pending_confessions.json
- comments.json
- contacts.json

Note: This will remove data required for production use. This script is intended for testing.
"""

import argparse
import os
import shutil
import time
from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parents[1]
FILES = [
    REPO_ROOT / 'approved_confessions.json',
    REPO_ROOT / 'pending_confessions.json',
    REPO_ROOT / 'comments.json',
    REPO_ROOT / 'contacts.json',
]

BACKUPS_DIR = REPO_ROOT / 'backups'


def backup_file(src: Path, dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    if src.exists():
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        dest = dest_dir / f"{src.name}.bak.{timestamp}"
        shutil.copy2(src, dest)
        print(f'Backed up {src.name} -> {dest.name}')
    else:
        print(f'No {src.name} file to back up.')


def clear_file(src: Path):
    # Write an empty JSON list
    with open(src, 'w') as f:
        json.dump([], f, indent=2)
    print(f'Cleared {src.name}')


def main(force=False, no_backup=False):
    print('🔄 Reset Test Database Script')
    print('Repo root:', REPO_ROOT)

    if not force:
        confirm = input('This will backup and clear test JSON files. Continue? [y/N]: ').strip().lower()
        if confirm not in ('y', 'yes'):
            print('Aborted by user.')
            return

    ts = time.strftime('%Y%m%d_%H%M%S')
    backup_subdir = BACKUPS_DIR / ts

    if not no_backup:
        for f in FILES:
            backup_file(f, backup_subdir)

    for f in FILES:
        clear_file(f)

    print('\n✅ Test DB reset complete.')
    print(f'Backups saved to: {backup_subdir}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reset test JSON DB files by backing up and clearing them.')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backups.')
    parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation prompt.')
    args = parser.parse_args()

    main(force=args.yes, no_backup=args.no_backup)
