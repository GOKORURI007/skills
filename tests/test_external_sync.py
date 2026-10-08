"""APM collection manifests must survive replacement by upstream sync."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def sync_module(repo_root):
    spec = importlib.util.spec_from_file_location(
        "sync_external_skills", repo_root / ".github/scripts/sync_external_skills.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_skill(root: Path, relative: str) -> None:
    folder = root / relative
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text("---\nname: example\n---\n", encoding="utf-8")


def test_collection_lists_categories_and_ignores_hidden_skills(sync_module, tmp_path):
    add_skill(tmp_path, "productivity/grill-me")
    add_skill(tmp_path, "engineering/tdd")
    add_skill(tmp_path, ".agents/skills/private")
    sync_module.write_apm_plugin(tmp_path, {"name": "collection", "version": "0.1.0"})
    plugin = json.loads((tmp_path / "plugin.json").read_text(encoding="utf-8"))
    assert plugin["skills"] == ["./engineering/tdd", "./productivity/grill-me"]


def test_empty_collection_fails_instead_of_silent_empty_install(sync_module, tmp_path):
    with pytest.raises(ValueError, match="No skills found"):
        sync_module.write_apm_plugin(tmp_path, {"name": "empty"})


def test_sync_regenerates_plugin_after_replacing_upstream(sync_module, tmp_path, monkeypatch):
    target = tmp_path / "skills/collection"
    add_skill(target, "old/removed")
    (target / "plugin.json").write_text('{"skills": ["./old/removed"]}')
    manifest = {
        "skills": [{
            "source": "https://github.com/example/collection.git",
            "source_path": "skills",
            "target_path": "skills/collection",
            "apm_plugin": {"name": "collection", "version": "0.1.0"},
        }]
    }
    (tmp_path / "external_skills.json").write_text(json.dumps(manifest))

    def clone_stub(url, ref, dest):
        add_skill(dest / "skills", "engineering/new-skill")

    monkeypatch.setattr(sync_module, "clone_to", clone_stub)
    monkeypatch.setattr("sys.argv", ["sync", "--workdir", str(tmp_path)])
    assert sync_module.main() == 0
    plugin = json.loads((target / "plugin.json").read_text())
    assert plugin["skills"] == ["./engineering/new-skill"]
    assert not (target / "old").exists()


def test_apm_only_does_not_download_or_replace_skills(sync_module, tmp_path, monkeypatch):
    target = tmp_path / "skills/collection"
    add_skill(target, "productivity/keep")
    (tmp_path / "external_skills.json").write_text(json.dumps({"skills": [{
        "target_path": "skills/collection", "apm_plugin": {"name": "collection"}
    }]}))
    monkeypatch.setattr("sys.argv", ["sync", "--workdir", str(tmp_path), "--apm-only"])
    assert sync_module.main() == 0
    assert (target / "productivity/keep/SKILL.md").exists()
    assert json.loads((target / "plugin.json").read_text())["skills"] == ["./productivity/keep"]


def test_committed_plugins_cover_current_upstream_skills(repo_root, sync_module, tmp_path):
    manifest = json.loads((repo_root / "external_skills.json").read_text(encoding="utf-8"))
    for entry in manifest["skills"]:
        if "apm_plugin" not in entry:
            continue
        target = repo_root / entry["target_path"]
        plugin = json.loads((target / "plugin.json").read_text(encoding="utf-8"))
        expected = sorted(
            "./" + skill.parent.relative_to(target).as_posix()
            for skill in target.rglob("SKILL.md")
            if not any(part.startswith(".") for part in skill.relative_to(target).parts)
        )
        assert plugin == {**entry["apm_plugin"], "skills": expected}
        assert len(expected) == len(set(expected))
