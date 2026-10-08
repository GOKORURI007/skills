---
name: add-external-skill
description: Add an upstream skill to this repository's synchronized APM collections.
disable-model-invocation: true
---

# Add an external skill

Read root `apm.yml`, `external_skills.json`, the chosen category's `apm.yml`, and README before editing.

1. Locate the upstream repository and skill directory on its current default branch. Verify `SKILL.md`, required resources, and license information. Preserve upstream skill instructions and resources when mirroring.
2. Add the directory mapping to `external_skills.json`, grouped under its `repository`. Set `path` to the source skill directory (or `.`) and `target` to `packages/<category>/skills/<name>`. Sync follows default branch HEAD; the configuration has no revision pins. Targets and skill names within a category must be unique.
3. Keep category `apm.yml` metadata-only. Register new categories in root `marketplace.packages` with local `./packages/<category>` sources. Marketplace entries represent collections; individual skills are selected through APM's `--skill` without separate entries or wrapper packages.
4. Run `python .github/scripts/sync_external_skills.py`. All upstream downloads and selected directories must validate before mirrors are replaced. If an upstream skill disappeared, resolve its new location or remove its mapping and mirrored directory; do not silently use an older commit. Update README membership and counts.
5. Run the sync tests, `apm marketplace check --offline`, and `apm pack --offline`; verify generated catalogs with `apm pack --check-clean --offline`. Test the affected collection and its `--skill` selection in a temporary consumer project, including resources.

Completion: the mirrored skill and resources are present, the category exposes selectable native skills, the generated catalogs match root YAML, and the consumer receives the selected members. Commit or push only when authorized by the user.

Consumers only need APM. To remove an individual member, edit the dependency's `skills:` keep-list in the consumer's `apm.yml` and run `apm install`. `apm update` refreshes the collection while preserving that selection; `apm uninstall` removes the whole collection. Keep maintainer sync commands out of consumer installation steps.
