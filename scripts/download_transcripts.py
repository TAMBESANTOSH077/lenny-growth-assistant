"""Download a public Lenny transcript archive using git.

Run from the project root:
    python scripts/download_transcripts.py
"""
import shutil
import subprocess
from pathlib import Path

URL = "https://github.com/doncampbell/lennys-podcast-transcripts.git"
DEST = Path(__file__).resolve().parents[1] / "data" / "transcripts"

if DEST.exists() and any(DEST.iterdir()):
    print(f"{DEST} already contains files; refusing to overwrite.")
    raise SystemExit(0)

tmp = DEST.parent / "_lenny_archive"
subprocess.run(["git", "clone", "--depth", "1", URL, str(tmp)], check=True)
episodes = tmp / "episodes"
DEST.mkdir(parents=True, exist_ok=True)
for src in episodes.rglob("*"):
    if src.is_file() and src.suffix.lower() in {".md", ".txt"}:
        target = DEST / src.name
        shutil.copy2(src, target)
print(f"Downloaded transcripts to {DEST}")
