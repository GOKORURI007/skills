#!/usr/bin/env python3
"""Mirror selected upstream skills into native APM collections (stdlib only).

Every source is fetched from its default branch HEAD. All downloads and skill
directories are validated before any tracked mirror directory is replaced.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
import urllib.request
import zipfile


def child(root, relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or "\\" in relative or ":" in relative:
        raise ValueError(f"Unsafe relative path: {relative}")
    target = root.joinpath(*path.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes root: {relative}")
    return target


def load_config(path, root):
    config = json.loads(path.read_text(encoding="utf-8"))
    if config.get("version") != 1:
        raise ValueError("Unsupported external_skills.json version")
    repositories, targets = set(), set()
    for source in config["sources"]:
        repository = source["repository"]
        if set(source) != {"repository", "skills"} or not re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
            raise ValueError(f"Expected repository and skills, with no pinned ref: {source}")
        if repository.lower() in repositories:
            raise ValueError(f"Duplicate repository: {repository}")
        repositories.add(repository.lower())
        for skill in source["skills"]:
            target = skill["target"]
            if not re.fullmatch(r"packages/[\w-]+/skills/[\w-]+", target):
                raise ValueError(f"Invalid mirror target: {target}")
            if target.lower() in targets:
                raise ValueError(f"Duplicate mirror target: {target}")
            targets.add(target.lower())
            child(root, target)
            child(root, skill["path"])
            if not (root / PurePosixPath(target).parents[1] / "apm.yml").is_file():
                raise ValueError(f"Missing category manifest for {target}")
    return config["sources"]


def extract_archive(archive, destination):
    with zipfile.ZipFile(archive) as bundle:
        roots = {PurePosixPath(item.filename).parts[0] for item in bundle.infolist()}
        if len(roots) != 1:
            raise ValueError("Expected a GitHub archive with one root directory")
        for item in bundle.infolist():
            relative = PurePosixPath(item.filename)
            child(destination, item.filename)
            if stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError(f"Symlink in upstream archive: {item.filename}")
            if ".git" in relative.parts:
                continue
            target = child(destination, PurePosixPath(*relative.parts[1:]).as_posix())
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with bundle.open(item) as reader, target.open("wb") as writer:
                    shutil.copyfileobj(reader, writer)
                mode = (item.external_attr >> 16) & 0o777
                if mode:
                    target.chmod(mode)


def download(repository, destination):
    archive = destination.with_suffix(".zip")
    request = urllib.request.Request(
        f"https://codeload.github.com/{repository}/zip/HEAD",
        headers={"User-Agent": "ruri-skills-sync"},
    )
    print(f"Fetching {repository} default branch", flush=True)
    with urllib.request.urlopen(request, timeout=90) as response, archive.open("wb") as writer:
        shutil.copyfileobj(response, writer)
    destination.mkdir()
    extract_archive(archive, destination)
    return destination


def sync(config_path, root, fetch=download):
    root = root.resolve()
    sources = load_config(config_path, root)
    with tempfile.TemporaryDirectory(prefix="ruri-skills-sync-") as temporary:
        staging = Path(temporary)
        with ThreadPoolExecutor(max_workers=4) as pool:
            jobs = [(source, pool.submit(fetch, source["repository"], staging / str(index)))
                    for index, source in enumerate(sources)]
            fetched = [(source, job.result()) for source, job in jobs]
        replacements = []
        for source, checkout in fetched:
            for skill in source["skills"]:
                origin = child(checkout, skill["path"])
                if not (origin / "SKILL.md").is_file():
                    raise ValueError(f"Missing SKILL.md: {source['repository']}/{skill['path']}")
                target = child(root, skill["target"])
                prepared = staging / ("prepared-" + str(len(replacements)))
                shutil.copytree(origin, prepared, ignore=shutil.ignore_patterns(".git"))
                # Subdirectory exports retain the repository's license and notices.
                if origin != checkout:
                    for license_file in checkout.iterdir():
                        if license_file.is_file() and re.match(r"^(LICENSE|LICENCE|COPYING|NOTICE)([._-]|$)", license_file.name, re.I):
                            if not (prepared / license_file.name).exists():
                                shutil.copy2(license_file, prepared / license_file.name)
                replacements.append((prepared, target, skill["target"]))
        for prepared, target, relative in replacements:
            # Recheck containment immediately before replacing a managed directory.
            child(root, relative)
            if target.exists():
                shutil.rmtree(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(prepared, target)
        print(f"Synced {len(replacements)} skills from {len(sources)} default branches.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", default="external_skills.json")
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        sync(args.workdir / args.manifest, args.workdir)
    except Exception as error:
        print(f"Sync failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
