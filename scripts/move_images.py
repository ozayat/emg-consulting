#!/usr/bin/env python3
"""
scripts/move_images.py

Move image files from the repository root into an `images/` folder, update references
in common text files (.html, .htm, .js, .css, .md), and optionally remove duplicate
image files (by content hash).

Usage (run from repository root after cloning):

  python3 scripts/move_images.py --dry-run
  python3 scripts/move_images.py        # actually performs changes

Notes:
- This script does not run `git` commands. After running it you should review changes
  and commit them with `git add -A && git commit -m "Move images into images/"`.
- The script tries to use `git mv` when available to preserve history. If `git mv`
  is not available (or you run outside a git repo), it will fall back to shutil.move.
- It updates references by plain string replacement of filenames. Please review
  changed files before committing.
- Duplicate deletion: when multiple files have identical content, the script keeps
  the first encountered and removes the duplicates (and replaces references to
  duplicate names with the kept name).

This is a convenience tool so I can safely perform the reorganization locally or
in a branch if you want me to make the commits for you. You previously confirmed
Option B / default branch / delete duplicates — I added this script to implement
that. Run it locally or tell me if you want me to run it and commit the changes
directly in a branch.
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
from pathlib import Path

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.tif', '.tiff', '.svg', '.webp', '.bmp', '.emf'}
TEXT_FILE_EXTS = {'.html', '.htm', '.js', '.css', '.md', '.txt', '.json'}

ROOT = Path('.')
IMAGES_DIR = Path('images')
SCRIPTS_DIR = Path('scripts')


def is_image_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in IMAGE_EXTS


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def find_repo_files():
    # find candidate image files in repository root and top-level only
    # (avoids touching files already in subdirectories named images etc.)
    images = []
    other_text_files = []
    for p in ROOT.iterdir():
        if p.name == 'images' or p.name == 'scripts':
            continue
        if is_image_file(p):
            images.append(p)
        elif p.is_file() and p.suffix.lower() in TEXT_FILE_EXTS:
            other_text_files.append(p)
    # also scan subdirectories for references to update
    for root, dirs, files in os.walk('.', topdown=True):
        # skip .git and images folder
        if root.startswith('./.git') or '/.git/' in root:
            continue
        if root.startswith('./images'):
            continue
        for fname in files:
            p = Path(root) / fname
            if p.suffix.lower() in TEXT_FILE_EXTS and p not in other_text_files:
                other_text_files.append(p)
    return images, other_text_files


def try_git_mv(src: Path, dst: Path) -> bool:
    try:
        subprocess.run(['git', 'mv', str(src), str(dst)], check=True)
        return True
    except Exception:
        return False


def update_references(text_paths, replacements, dry_run=False):
    # replacements: dict of old_name -> new_name
    pattern = re.compile('|'.join(re.escape(k) for k in replacements.keys()))
    changed_files = []
    for path in text_paths:
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            # skip binary or unreadable files
            continue
        new_text, n = pattern.sub(lambda m: replacements[m.group(0)], text), 0
        # count occurrences by naive approach
        for old, new in replacements.items():
            n += text.count(old)
        if new_text != text:
            changed_files.append((path, n))
            if not dry_run:
                path.write_text(new_text, encoding='utf-8')
    return changed_files


def main():
    parser = argparse.ArgumentParser(description='Move images into an images/ folder and update references')
    parser.add_argument('--dry-run', action='store_true', help='Show actions without making changes')
    parser.add_argument('--keep-originals', action='store_true', help='Do not delete original files (use copies)')
    parser.add_argument('--no-git-mv', action='store_true', help='Do not attempt `git mv`, always move file system-wise')
    args = parser.parse_args()

    images, text_files = find_repo_files()

    if not images:
        print('No image files found in repository root to move.')
        return

    print(f'Found {len(images)} image files to consider moving into {IMAGES_DIR}/')
    print(f'Scanning {len(text_files)} text files to update references.')

    # compute hashes to detect duplicates
    hash_map = {}
    basename_map = {}
    for p in images:
        h = file_hash(p)
        hash_map.setdefault(h, []).append(p)
        basename_map.setdefault(p.name, []).append(p)

    # decide which files to keep when duplicates exist
    keep_map = {}  # mapping from Path kept -> list of duplicate Paths removed
    for h, paths in hash_map.items():
        if len(paths) > 1:
            # keep first, remove others
            keeper = paths[0]
            duplicates = paths[1:]
            keep_map[keeper] = duplicates

    # build replacement mapping: old filename -> images/<filename-kept>
    replacements = {}

    # ensure images dir exists (in dry-run, just report)
    if not args.dry_run:
        IMAGES_DIR.mkdir(exist_ok=True)

    for p in images:
        # determine final filename: if this file is a duplicate of a keeper, map to keeper
        h = file_hash(p)
        keeper = None
        for k, dup_list in keep_map.items():
            if p in dup_list:
                keeper = k
                break
        if keeper is not None:
            # this file is a duplicate and will be removed; map its basename to keeper's new path
            new_rel = str(Path('images') / keeper.name)
            replacements[p.name] = new_rel
            print(f'Planned duplicate: {p} -> keep {keeper.name}')
        else:
            # unique or keeper itself: move to images/<basename>
            new_rel = str(Path('images') / p.name)
            replacements[p.name] = new_rel

    # update references first (so references to duplicates are updated to keeper name)
    print('\nReference replacement plan:')
    for old, new in list(replacements.items())[:20]:
        print(f'  {old} -> {new}')
    if len(replacements) > 20:
        print(f'  ... ({len(replacements)-20} more)')

    changed = update_references(text_files, replacements, dry_run=args.dry_run)
    print(f'Updated references in {len(changed)} files (dry-run={args.dry_run}).')

    # move files
    moved = []
    removed = []
    for p in images:
        # if this file is a duplicate and not the keeper, remove it after references updated
        is_dup = any(p in dups for dups in keep_map.values())
        if is_dup:
            if args.dry_run:
                print(f'[dry-run] Would remove duplicate {p}')
            else:
                try:
                    p.unlink()
                    removed.append(p)
                    print(f'Removed duplicate {p}')
                except Exception as e:
                    print(f'Failed to remove {p}: {e}')
            continue

        dst = IMAGES_DIR / p.name
        if args.dry_run:
            print(f'[dry-run] Would move {p} -> {dst}')
            moved.append((p, dst))
        else:
            moved_ok = False
            if not args.no_git_mv:
                moved_ok = try_git_mv(p, dst)
            if not moved_ok:
                try:
                    shutil.move(str(p), str(dst))
                    moved.append((p, dst))
                    print(f'Moved {p} -> {dst}')
                except Exception as e:
                    print(f'Failed to move {p} -> {dst}: {e}')

    print('\nSummary:')
    print(f'  Files moved: {len(moved)}')
    print(f'  Duplicates removed: {len(removed)}')
    print('Next steps:')
    print('  - Review the changed files and `git status`/`git diff` in your clone.')
    print('  - If everything looks good, commit:')
    print("      git add -A && git commit -m 'Move images into images/ and update references'")
    print('  - Push and open a pull request if you prefer changes on a branch.')

if __name__ == '__main__':
    main()
