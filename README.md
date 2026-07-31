# Juno-Pipeline

A Houdini-centric VFX and animation pipeline built around layered configuration, resolved paths, and reproducible show structure. Juno treats Houdini as the center of the pipeline and other DCCs (Maya, etc.) as clients, and is designed to run natively across macOS, Linux, and Windows.

> **Status:** Active development. The configuration and path-resolution layers and the show/sequence/shot scaffolding tools are complete and tested. Publishing, schema validation at load time, and DCC integration are on the roadmap below.

---

## Why Juno

Juno is both a working pipeline and a study in doing pipeline architecture the way a facility actually does it. Rather than hardcoding paths and settings, everything flows from a small set of deliberate principles:

- **Paths are resolved, never constructed.** No tool builds a path by gluing strings together. Named templates describe the folder layout, and a single resolver fills them — so the structure lives in exactly one place.
- **Configuration is layered and sparse.** A resolved config is built by merging, most-specific-wins: pipeline defaults → project → shot. Override files contain *only* what differs; a shot with no overrides has no override file at all.
- **Single source of truth.** Pipeline defaults are extracted directly from the JSON Schema that documents and validates them, so defaults and documentation can never drift apart. Shared schema definitions are referenced (`$ref`), never duplicated.
- **Publishes are immutable and versioned.** Published data is append-only and never overwritten — new work becomes a new version. (Publishing tooling is on the roadmap; the folder structure that supports it is already scaffolded.)
- **Site vs. show separation.** Machine-specific locations (where `/show` lives, where the pipeline lives) come from the environment. Show-specific settings come from config. Code reads both and hardcodes neither.
- **Fail loudly, fail clearly.** Missing environment, missing parents, and name collisions raise immediately with actionable messages, rather than producing broken structure downstream.

---

## Architecture

Juno is organized into three layers, each building on the one below it.

### 1. Configuration resolution

Given a show's config files, produce a single fully-resolved settings object.

- **Schemas** (`config/schema/`) validate, document, and supply defaults for every field. A shared `common.schema.json` holds reusable definitions (`format`, `frames`, `color`, `fx`) that the project, shot, and asset schemas reference via `$ref`.
- **Default extraction** walks the schema and pulls out every `default` value to form the base layer — so the defaults are derived from the schema, not maintained separately.
- **Deep merge** folds each layer onto the last, recursing into nested objects and letting the most-specific layer win, while lists replace wholesale and inputs are never mutated.

The result: `defaults → project.json → shot.json`, collapsed into one config where every value traces back to the most-specific layer that set it.

### 2. Path resolution

Turn identifiers into real filesystem paths.

- **Roots come from the environment** — `JUNO_SHOW_ROOT` (where shows live) and `JUNO_PIPELINE_ROOT` (where the pipeline lives). This is the site-specific layer, set by a launcher in production and by the shell in development.
- **Templates** (`config/templates.json`) describe the folder layout as named patterns with `{tokens}`. A single token-agnostic resolver fills any template with any tokens and prepends the show root, returning a complete `Path`.

Because the resolver knows every path pattern, tools ask for locations by name and identifier rather than knowing the folder structure themselves.

### 3. Scaffolding

Create consistent show structure on disk, using the two layers above.

- `scaffold_show` — creates the show root, `config/`, `sequences/`, and `assets/`, and writes a minimal `project.json`.
- `scaffold_sequence` — creates a sequence inside a show.
- `scaffold_shot` — creates a shot with a `config/` folder and, for each department the show uses, a `_work` and `_publish` area. The department list is read from the show's resolved config, so scaffolding respects each show's setup rather than hardcoding it.

Every scaffold operation checks that its parent exists and that it does not already exist, so orphaned or clobbered structure is impossible.

---

## The resolution flow

```
identifiers ──► resolve_template ──► file paths ──► config resolver ──► resolved config
   (show,          (roots +                            (defaults →
    sequence,       templates)                          project →
    shot)                                               shot, merged)
```

The same path resolution also drives scaffolding: identifiers become paths, and paths become created structure.

---

## Project structure

```
juno-pipeline/
├── python/juno/            # the juno package
│   ├── utils.py            # shared low-level helpers (load_config)
│   ├── config.py           # config resolution, deep merge, default extraction
│   ├── paths.py            # environment roots, template resolution
│   └── scaffolding.py      # show / sequence / shot creation
├── config/
│   ├── schema/             # JSON Schemas (common, project, shot, asset)
│   ├── templates.json      # path templates
│   └── examples/           # example project.json / shot.json
├── tests/                  # pytest suite
├── docs/DEVELOPMENT.md     # session setup and workflow
└── pyproject.toml
```

---

## Setup

Juno targets **Python 3.13**, matching Houdini 22 and the VFX Reference Platform CY2026.

```bash
# from the repo root
python3.13 -m venv .venv
source .venv/bin/activate            # macOS / Linux
pip install -e ".[dev]"              # install juno plus dev tools (pytest)
```

Set the two environment roots for your machine:

```bash
export JUNO_SHOW_ROOT=/path/to/show
export JUNO_PIPELINE_ROOT=/path/to/juno-pipeline
```

Run the tests:

```bash
pytest
```

See [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) for the full session workflow.

---

## Tech stack

- **Language:** Python 3.13 (VEX and PyQt/PySide planned)
- **Primary DCC:** Houdini 22 / Solaris; Maya as a client
- **Scene description:** USD (planned integration)
- **Color:** OCIO / ACEScg
- **Config validation:** JSON Schema (`jsonschema`)
- **Testing:** pytest
- **Reference:** VFX Reference Platform CY2026

---

## Roadmap

**Built**
- [x] Layered configuration schema with shared `$ref` definitions
- [x] Schema-driven default extraction
- [x] Deep-merge config cascade (defaults → project → shot)
- [x] Environment-based path roots and template resolution
- [x] Resolve a shot's full config by identifier
- [x] Show / sequence / shot scaffolding with existence guards
- [x] Test suite for config, paths, and scaffolding

**Planned**
- [ ] Schema validation at load time (fail loudly on malformed config)
- [ ] Naming-convention enforcement in scaffolding
- [ ] Immutable, versioned publish tooling
- [ ] Cache-tier promotion (scratch → shared → publish)
- [ ] Per-show pipeline versioning
- [ ] USD / Solaris layer strategy
- [ ] Houdini packages and HDA publishing workflow
- [ ] PySide browser / publish tools
- [ ] Cross-platform validation on Linux and Windows

---

## Development notes

Juno is developed on macOS with a Windows/Linux workstation targeted for Houdini simulation work. The tool stack (Houdini, Maya, USD, Python) runs natively across all three platforms; the pipeline is written to be path-root- and separator-agnostic so the same code runs everywhere.