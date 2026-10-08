---
name: add-external-skill
description: Add an upstream skill to this repository's APM marketplace and category package.
disable-model-invocation: true
---

# Add an external skill

Maintain this repository's APM marketplace. Read root `apm.yml`, the appropriate `packages/<category>/apm.yml`, and README before editing.

1. Resolve the upstream Git repository, default branch and desired skill directory. Verify the directory contains `SKILL.md` and inspect any sibling resources it needs.
2. Choose an existing category or add a category package when none fits. Add a dependency with `git` and optional `path` to the category's `dependencies.apm`. Omit `ref` to follow the latest default branch; use a moving branch only when a specific branch is required. Keep upstream content upstream.
3. Register only category bundles in root `marketplace.packages`, with a unique `name`, local `./packages/<category>` source, version, `description`, and `category`. Individual skills are selected with APM's `--skill`, without single-skill marketplace entries or wrapper manifests.
4. Update README category membership. Run `apm marketplace check` and `apm pack`; inspect both generated market files. Verify the new skill and category package install in a temporary consumer project, including their resources.

Completion: the category dependency follows a moving upstream branch and the verified directory, generated catalogs contain only the bundles declared in root YAML, and the isolated consumer receives the expected skills. Commit or push only when the user's request authorizes it.

Native first-party collections support `apm install <bundle>@ruri-skills --skill <name>`. For external skills, use `apm install <upstream-collection> --skill <upstream-name-or-path>` and verify the upstream exposes that selection; dependency-only category packages do not forward `--skill` to their dependencies. Use the upstream's actual skill name, without a marketplace prefix. Consult `apm ... --help` and the [APM install reference](https://microsoft.github.io/apm/reference/cli/install/) for supported selections. Consumer lockfiles record resolved commits; `apm update` refreshes floating dependencies.
