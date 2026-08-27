#!/usr/bin/env python3
"""
Sync external skills defined in external_skills.json into this repo.

For each entry:
  - clone source repo (shallow, single branch)
  - copy source_path contents into target_path (incremental overlay)

The script only touches target_path directories declared in the manifest and
leaves all other paths in the repo untouched.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def normalize_source(source: str) -> str:
    s = source.strip()
    if s.startswith("git@") or s.startswith("ssh://"):
        return s
    if s.startswith("http://") or s.startswith("https://"):
        return s if s.endswith(".git") else s + ".git"
    # bare form: host/owner/repo
    return f"https://{s}.git"


def clone_to(url: str, ref: str, dest: Path) -> None:
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", ref, url, str(dest)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def repo_slug(url: str) -> str:
    tail = url.rstrip("/").rsplit("/", 1)[-1]
    return tail[:-4] if tail.endswith(".git") else tail


def remove_path(p: Path) -> None:
    if p.is_symlink() or p.is_file():
        p.unlink()
    elif p.exists():
        shutil.rmtree(p)


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync external skills.")
    ap.add_argument(
        "manifest",
        nargs="?",
        type=Path,
        default=Path("external_skills.json"),
        help="path to external_skills.json (default: ./external_skills.json)",
    )
    ap.add_argument(
        "--workdir",
        type=Path,
        default=Path("."),
        help="working directory (default: current directory)",
    )
    args = ap.parse_args()

    manifest_path = args.workdir / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    skills = manifest.get("skills", [])

    failures = 0
    with tempfile.TemporaryDirectory(prefix="ext-skill-") as tmp_str:
        tmp = Path(tmp_str)
        for entry in skills:
            source = entry["source"]
            source_path = entry["source_path"].strip(".") or "."
            target_path = args.workdir / entry["target_path"]
            ref = entry.get("ref", "main")
            url = normalize_source(source)
            slug = repo_slug(url)
            clone_dir = tmp / slug

            print(f"[sync] {slug}: clone {url} @ {ref}", flush=True)
            try:
                clone_to(url, ref, clone_dir)
            except subprocess.CalledProcessError as exc:
                failures += 1
                print(
                    f"[sync] WARN: clone failed for {url} ({ref}): "
                    f"{exc.stderr.decode(errors='replace')}",
                    file=sys.stderr,
                    flush=True,
                )
                continue

            src_dir = clone_dir / source_path if source_path != "." else clone_dir
            if not src_dir.exists():
                failures += 1
                print(
                    f"[sync] WARN: '{source_path}' not found in {slug}, skipping",
                    file=sys.stderr,
                    flush=True,
                )
                continue

            remove_path(target_path)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(
                src_dir,
                target_path,
                ignore=shutil.ignore_patterns(".git"),
            )
            print(f"[sync] {slug}: copied to {target_path}", flush=True)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())