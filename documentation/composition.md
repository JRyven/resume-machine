---
project_name: Resume Machine
title: Composition Engine
description:
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords:
---

This document explains how to use the composition and build scripts.

Usage examples

1. Compose YAML fragments into JSON Resume

```bash
python scripts/compose_resume.py \
  --base content/base.yaml \
  --fragments content/fragments/experience/goop.yaml content/fragments/skills/full-stack.yaml \
  -o build/resume.json \
  --validate schema/jsonresume-schema.json
```

2. Build PDF (dry-run)

```bash
python scripts/build_resume.py --base content/base.yaml --role senior-engineer --output-dir artifacts --dry-run
```

Notes

- The composer implements deep-merge rules: dicts are merged, lists are extended, scalars are overridden by fragments.
- `build_resume.py` writes a sidecar metadata file `resume.metadata.json` to avoid visible generation timestamps in the PDF body.
- For real PDF generation `resumed` must be installed and available on PATH.
