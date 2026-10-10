import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import yaml


spec = importlib.util.spec_from_file_location(
    "generate_marketplace_descriptions",
    Path(__file__).resolve().parents[1] / ".github/scripts/generate_marketplace_descriptions.py",
)
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)


class DescriptionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        config = self.root / ".github/scripts/marketplace_descriptions.json"
        config.parent.mkdir(parents=True)
        config.write_text(json.dumps({"introductions": {"example": "开发工具。"}, "summaries": {}}), encoding="utf-8")
        (self.root / "apm.yml").write_text(
            '# Preserve this comment\nname: test\nmarketplace:\n  packages:\n'
            '    - name: example\n      source: "./packages/example"\n'
            '      description: "old"\n      category: Development\n', encoding="utf-8",
        )
        for relative in (".claude-plugin/marketplace.json",):
            path = self.root / relative
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"plugins": [{"name": "example", "description": "old", "source": "./packages/example"}]}), encoding="utf-8")
        self.skill("z", 'description: >-\n  第一行介绍。\n  这是触发条件。')
        self.skill("a", 'name: different-name\ndescription: "简短说明：支持 Git。后续触发条件。"')

    def skill(self, name, metadata):
        path = self.root / f"packages/example/skills/{name}/SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{metadata}\n---\n正文", encoding="utf-8")
        return path

    def test_sorted_top_level_members_multiline_and_idempotence(self):
        self.skill("a/references/nested", "description: 不应列出。")
        generator.generate(self.root)
        text = (self.root / "apm.yml").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Preserve this comment\n"))
        description = yaml.safe_load(text)["marketplace"]["packages"][0]["description"]
        self.assertEqual(description, "开发工具。\n技能：\n- a: 简短说明：支持 Git。\n- z: 第一行介绍。")
        for relative in (".claude-plugin/marketplace.json",):
            data = json.loads((self.root / relative).read_text(encoding="utf-8"))
            self.assertEqual(data["plugins"][0]["description"], description)
        generator.generate(self.root, check=True)
        generator.generate(self.root)
        self.assertEqual((self.root / "apm.yml").read_text(encoding="utf-8"), text)

    def test_changed_and_removed_skills_update_inventory(self):
        generator.generate(self.root)
        path = self.skill("a", "description: 新说明。")
        with self.assertRaisesRegex(ValueError, "Outdated descriptions"):
            generator.generate(self.root, check=True)
        path.unlink()
        path.parent.rmdir()
        generator.generate(self.root)
        self.assertNotIn("- a:", (self.root / "apm.yml").read_text(encoding="utf-8"))

    def test_invalid_skill_preserves_outputs(self):
        manifest = self.root / "apm.yml"
        original = manifest.read_bytes()
        self.skill("invalid", "name: invalid")
        with self.assertRaisesRegex(ValueError, "Missing description"):
            generator.generate(self.root)
        self.assertEqual(manifest.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
