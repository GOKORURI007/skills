import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location("sync_external_skills", Path(__file__).resolve().parents[1] / ".github/scripts/sync_external_skills.py")
syncer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(syncer)


class SyncTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.category = self.root / "packages/example"
        self.category.mkdir(parents=True)
        (self.category / "apm.yml").write_text("name: example\n")
        self.target = self.category / "skills/one"
        self.target.mkdir(parents=True)
        (self.target / "SKILL.md").write_text("old")
        (self.target / "removed.txt").write_text("stale")
        self.manifest = self.root / "external_skills.json"
        self.config = {"version": 1, "sources": [{"repository": "owner/repo", "skills": [{"path": "skills/one", "target": "packages/example/skills/one"}]}]}
        self.save()

    def save(self):
        self.manifest.write_text(json.dumps(self.config))

    def fetch(self, repo, destination):
        skill = destination / "skills/one"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("new")
        (skill / "assets").mkdir()
        (skill / "assets/data.bin").write_bytes(b"\x00\xff")
        (destination / "LICENSE").write_text("upstream license")
        return destination

    def test_sync_replaces_stale_files_and_preserves_resources(self):
        own = self.category / "skills/own/SKILL.md"
        own.parent.mkdir()
        own.write_text("first party")
        syncer.sync(self.manifest, self.root, self.fetch)
        self.assertEqual((self.target / "SKILL.md").read_text(), "new")
        self.assertFalse((self.target / "removed.txt").exists())
        self.assertEqual((self.target / "assets/data.bin").read_bytes(), b"\x00\xff")
        self.assertEqual((self.target / "LICENSE").read_text(), "upstream license")
        self.assertEqual(own.read_text(), "first party")

    def test_missing_skill_preserves_all_existing_mirrors(self):
        self.config["sources"][0]["skills"].append({"path": "skills/missing", "target": "packages/example/skills/missing"})
        self.save()
        with self.assertRaisesRegex(ValueError, "Missing SKILL.md"):
            syncer.sync(self.manifest, self.root, self.fetch)
        self.assertEqual((self.target / "SKILL.md").read_text(), "old")
        self.assertTrue((self.target / "removed.txt").exists())

    def test_download_failure_preserves_existing_mirrors(self):
        def fail(repo, destination):
            raise OSError("network failure")
        with self.assertRaises(OSError):
            syncer.sync(self.manifest, self.root, fail)
        self.assertEqual((self.target / "SKILL.md").read_text(), "old")

    def test_rejects_pinned_ref(self):
        self.config["sources"][0]["ref"] = "abc123"
        self.save()
        with self.assertRaisesRegex(ValueError, "no pinned ref"):
            syncer.load_config(self.manifest, self.root)

    def test_rejects_duplicate_targets(self):
        self.config["sources"][0]["skills"] *= 2
        self.save()
        with self.assertRaisesRegex(ValueError, "Duplicate mirror"):
            syncer.load_config(self.manifest, self.root)

    def test_rejects_target_traversal(self):
        self.config["sources"][0]["skills"][0]["target"] = "packages/example/skills/../../outside"
        self.save()
        with self.assertRaises(ValueError):
            syncer.load_config(self.manifest, self.root)

    def test_rejects_archive_traversal_and_symlinks(self):
        for name, symlink in [("repo/../../escape", False), ("repo/link", True)]:
            with self.subTest(name=name):
                archive = self.root / "source.zip"
                with zipfile.ZipFile(archive, "w") as bundle:
                    info = zipfile.ZipInfo(name)
                    if symlink:
                        info.external_attr = 0o120777 << 16
                    bundle.writestr(info, "payload")
                with self.assertRaises(ValueError):
                    syncer.extract_archive(archive, self.root / "extracted")

    def test_archive_preserves_binary_resources(self):
        archive = self.root / "source.zip"
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.writestr("repo/skills/one/SKILL.md", "skill")
            bundle.writestr("repo/skills/one/image.bin", b"\x00\xff")
        destination = self.root / "extracted"
        syncer.extract_archive(archive, destination)
        self.assertEqual((destination / "skills/one/image.bin").read_bytes(), b"\x00\xff")


if __name__ == "__main__":
    unittest.main()
