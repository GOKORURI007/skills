---
name: add-external-skill
description: Add an upstream skill to this repository's APM marketplace and category package.
disable-model-invocation: true
---

# Add an external skill

Maintain this repository's APM marketplace. Read root `apm.yml`, the appropriate `packages/<category>/apm.yml`, and README before editing.

1. Resolve the upstream Git repository, default branch and desired skill directory. Verify the directory contains `SKILL.md` and inspect any sibling resources it needs. Resolve the chosen ref to a commit with `git ls-remote`; use that commit in both manifests.
2. Choose an existing category or add a category package when none fits. Add a dependency with `git`, `ref`, and optional `path` to the category's `dependencies.apm`. Reference the skill's directory directly; keep upstream content upstream.
3. Create `packages/<category>/items/<name>/apm.yml` with that same single upstream dependency. Register it in root `marketplace.packages` with a unique `name`, local `./packages/<category>/items/<name>` source, wrapper version, `description`, and `category`. Matt Pocock entries use the `matt-` prefix. Register new category packages with a local `./packages/<category>` source.
4. Update README category membership. Run `apm marketplace check` and `apm pack`; inspect both generated market files. Verify the new skill and category package install in a temporary consumer project, including their resources.

Completion: the category dependency and single entry point to the same verified upstream commit and directory, the generated catalogs match root YAML, and the isolated consumer receives the expected skills. Commit or push only when the user's request authorizes it.

Native first-party collections support `--skill`; dependency-only category packages are selected through their individual marketplace entries. Consult `apm ... --help` and the [APM manifest reference](https://microsoft.github.io/apm/reference/manifest-schema/) for supported fields.
