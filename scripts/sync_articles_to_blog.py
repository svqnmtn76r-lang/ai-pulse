#!/usr/bin/env python3
import shutil
from pathlib import Path

SRC = Path("output/articles")
DST = Path("blog/src/content/articles")
DST.mkdir(parents=True, exist_ok=True)

synced = 0
for md_file in SRC.glob("*.md"):
    target = DST / md_file.name
    if not target.exists() or md_file.stat().st_mtime > target.stat().st_mtime:
        shutil.copy2(md_file, target)
        synced += 1

print(f"Synced {synced} articles to blog/")
