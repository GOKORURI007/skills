#!/usr/bin/env python3
"""Generate remote APM descriptions from top-level skills, without an AI service."""

import argparse
import json
from pathlib import Path
import re
import sys

import yaml


def skill_summary(path):
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    metadata = yaml.safe_load(match.group(1))
    description = metadata.get("description") if isinstance(metadata, dict) else None
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"Missing description: {path}")
    description = re.sub(r"\s+", " ", description).strip()
    # A short first sentence describes the capability, without lengthy triggers.
    sentence = re.split(r"(?<=[。！？])|(?<=[.!?])\s+", description, maxsplit=1)[0]
    return sentence if len(sentence) <= 160 else sentence[:159].rstrip() + "…"


def generate(root, check=False):
    root = root.resolve()
    config = json.loads((root / ".github/scripts/marketplace_descriptions.json").read_text(encoding="utf-8"))
    manifest_path = root / "apm.yml"
    original = manifest_path.read_text(encoding="utf-8")
    manifest = yaml.safe_load(original)
    descriptions = {}
    for package in manifest["marketplace"]["packages"]:
        name = package["name"]
        source = (root / package["source"]).resolve()
        if not source.is_relative_to(root / "packages"):
            raise ValueError(f"Package source must be inside packages/: {name}")
        skills = source / "skills"
        lines = [config["introductions"][name], "技能："]
        for directory in sorted(skills.iterdir(), key=lambda path: path.name):
            if not directory.is_dir():
                continue
            path = directory / "SKILL.md"
            summary = skill_summary(path)
            summary = config["summaries"].get(directory.name, summary)
            # Use the directory name accepted by --skill, not a possibly different
            # frontmatter name. Nested reference/example skills aren't members.
            lines.append(f"- {directory.name}: {summary}")
        if len(lines) == 2:
            raise ValueError(f"No skills found: {name}")
        descriptions[name] = "\n".join(lines)

    # Preserve all other YAML fields, comments and formatting. Only replace the
    # description scalar in each marketplace entry (not the root description).
    updated = original
    for name, description in descriptions.items():
        pattern = re.compile(
            r"(^    - name: " + re.escape(name) + r"\n(?:(?!    - name:).)*?^      description:)[^\n]*(?:\n(?:        [^\n]*|[ \t]*))*(?=\n\S|\n      \S|\n    - name:|\Z)",
            re.M | re.S,
        )
        replacement = " |-\n" + "\n".join("        " + line for line in description.splitlines())
        updated, count = pattern.subn(lambda match: match.group(1) + replacement, updated)
        if count != 1:
            raise ValueError(f"Expected one marketplace description for {name}, found {count}")
    parsed = yaml.safe_load(updated)
    if {p["name"]: p["description"] for p in parsed["marketplace"]["packages"]} != descriptions:
        raise ValueError("Generated YAML descriptions do not round-trip")
    outputs = {manifest_path: updated}
    # APM's Claude marketplace includes description. Its Codex pack output uses
    # a different schema and deliberately omits it; keep that artifact intact.
    for relative in (".claude-plugin/marketplace.json",):
        path = root / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        if {plugin["name"] for plugin in data["plugins"]} != set(descriptions):
            raise ValueError(f"Marketplace entries differ from apm.yml: {relative}")
        for plugin in data["plugins"]:
            plugin["description"] = descriptions[plugin["name"]]
        outputs[path] = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    changed = [path for path, text in outputs.items() if path.read_text(encoding="utf-8") != text]
    if check and changed:
        raise ValueError("Outdated descriptions: " + ", ".join(str(path.relative_to(root)) for path in changed))
    if not check:
        for path in changed:
            path.write_text(outputs[path], encoding="utf-8", newline="\n")
    print(f"Generated descriptions for {len(descriptions)} packages; {len(changed)} files changed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--check", action="store_true", help="Fail if generated descriptions are outdated")
    args = parser.parse_args()
    try:
        generate(args.workdir, args.check)
    except Exception as error:
        print(f"Generation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
