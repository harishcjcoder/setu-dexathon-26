"""
Creates an updated deployable zip archive containing all necessary
files for cloud deployment (Render, Hugging Face Spaces, Railway, Docker, or Cloud VM).
"""

import os
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_ZIP = ROOT_DIR / "sih2026_model_deployable.zip"

INCLUDED_ITEMS = [
    "config",
    "data",
    "models",
    "src",
    "ui",
    "Dockerfile",
    "docker-compose.yml",
    "render.yaml",
    "Procfile",
    "requirements.txt",
    "run.py",
    "run.bat",
    "README.md",
    ".dockerignore",
    ".env.example"
]

EXCLUDE_PATTERNS = [
    "__pycache__",
    ".pyc",
    ".git",
    ".pytest_cache",
    ".DS_Store",
    "tests"
]


def should_exclude(path: Path) -> bool:
    for part in path.parts:
        for pattern in EXCLUDE_PATTERNS:
            if pattern in part:
                return True
    return False


def main():
    print(f"[Packager] Generating {OUTPUT_ZIP.name} ...")
    count = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for item_name in INCLUDED_ITEMS:
            item_path = ROOT_DIR / item_name
            if not item_path.exists():
                print(f"  [Warning] Missing: {item_name}")
                continue

            if item_path.is_file():
                zf.write(item_path, arcname=item_name)
                count += 1
            elif item_path.is_dir():
                for sub_path in item_path.rglob("*"):
                    if sub_path.is_file() and not should_exclude(sub_path):
                        rel_path = sub_path.relative_to(ROOT_DIR)
                        zf.write(sub_path, arcname=str(rel_path).replace("\\", "/"))
                        count += 1

    file_size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"[Packager] Successfully packed {count} files into {OUTPUT_ZIP.name} ({file_size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
