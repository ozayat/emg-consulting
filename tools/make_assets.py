#!/usr/bin/env python3
"""Regenerate the derived reference assets from the original scans.

Everything this writes is reproducible from the 197 `EMG Reference List_Page_*.jpg`
files already in the repository, so the outputs never have to be moved by hand:

    assets/docs/EMG-Reference-Portfolio.pdf   the downloadable portfolio
    assets/img/reference/thumbs/page-NNN.jpg  contact-sheet thumbnails
    assets/img/reference/view/page-NNN.jpg    readable lightbox images

Requires Pillow:  pip install Pillow
Usage:            python3 tools/make_assets.py
"""
import glob
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_GLOB = "images/EMG Reference List_Page_*.jpg"

PDF_OUT = "assets/docs/EMG-Reference-Portfolio.pdf"
PDF_WIDTH, PDF_QUALITY = 1200, 68
THUMB_DIR, THUMB_BOX, THUMB_QUALITY = "assets/img/reference/thumbs", (520, 520), 76
VIEW_DIR, VIEW_WIDTH, VIEW_QUALITY = "assets/img/reference/view", 900, 72


def load_pages():
    os.chdir(ROOT)
    files = sorted(glob.glob(SOURCE_GLOB))
    if not files:
        sys.exit(f"No source scans matching {SOURCE_GLOB!r} in {ROOT}")
    print(f"{len(files)} source pages")
    return files


def build_pdf(files):
    os.makedirs(os.path.dirname(PDF_OUT), exist_ok=True)
    pages = []
    for f in files:
        im = Image.open(f).convert("RGB")
        if im.width > PDF_WIDTH:
            im = im.resize((PDF_WIDTH, round(im.height * PDF_WIDTH / im.width)), Image.LANCZOS)
        pages.append(im)
    pages[0].save(PDF_OUT, "PDF", save_all=True, append_images=pages[1:],
                  resolution=150, quality=PDF_QUALITY, optimize=True)
    print(f"  {os.path.getsize(PDF_OUT)/1024/1024:5.1f} MB  {PDF_OUT}")


def build_images(files):
    os.makedirs(THUMB_DIR, exist_ok=True)
    os.makedirs(VIEW_DIR, exist_ok=True)
    for i, f in enumerate(files, 1):
        im = Image.open(f).convert("RGB")

        thumb = im.copy()
        thumb.thumbnail(THUMB_BOX, Image.LANCZOS)
        thumb.save(f"{THUMB_DIR}/page-{i:03d}.jpg", "JPEG",
                   quality=THUMB_QUALITY, optimize=True, progressive=True)

        view = im.copy()
        if view.width > VIEW_WIDTH:
            view = view.resize((VIEW_WIDTH, round(view.height * VIEW_WIDTH / view.width)),
                               Image.LANCZOS)
        view.save(f"{VIEW_DIR}/page-{i:03d}.jpg", "JPEG",
                  quality=VIEW_QUALITY, optimize=True, progressive=True)
    print(f"  {len(files)} thumbnails -> {THUMB_DIR}")
    print(f"  {len(files)} view images -> {VIEW_DIR}")


if __name__ == "__main__":
    pages = load_pages()
    build_pdf(pages)
    build_images(pages)
    print("done — now run: python3 tools/build.py")
