#!/usr/bin/env python3
"""
Sync external skills defined in external_skills.json into this repo.

For each entry:
  - clone source repo (shallow, single branch)
  - replace target_path with source_path contents
  - generate configured APM collection manifests after copying

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


def write_apm_plugin(target_path: Path, metadata: dict) -> None:
    """Expose a categorized skill collection without moving upstream files."""
    skill_paths = sorted(
        "./" + skill.parent.relative_to(target_path).as_posix()
        for skill in target_path.rglob("SKILL.md")
        if not any(part.startswith(".") for part in skill.relative_to(target_path).parts)
    )
    if not skill_paths:
        raise ValueError(f"No skills found for APM collection: {target_path}")
    plugin = {**metadata, "skills": skill_paths}
    (target_path / "plugin.json").write_text(
        json.dumps(plugin, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync external skills.")
    ap.add_argument(
        "--apm-only",
        action="store_true",
        help="regenerate configured APM manifests without downloading upstream skills",
    )
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

    if args.apm_only:
        for entry in skills:
            if "apm_plugin" in entry:
                write_apm_plugin(args.workdir / entry["target_path"], entry["apm_plugin"])
        return 0

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
            if "apm_plugin" in entry:
                write_apm_plugin(target_path, entry["apm_plugin"])
            print(f"[sync] {slug}: copied to {target_path}", flush=True)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
