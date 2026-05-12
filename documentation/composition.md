---
project_name: Resume Machine
title: Composition Engine
description: Historical reference for the compose_resume.py / build_resume.py scripts (removed).
last_updated: 2026-05-12
cleardoc_version: 2.3.0
keywords: [composition, deprecated, compose_resume, build_resume]
---

# Composition Engine

**Path:** Documentation > Composition Engine

> **Deprecated.** The `compose_resume.py` and `build_resume.py` scripts described here have been removed. Resume generation is now handled by `src/data/py_skill_job_correlator.py` (correlation) and `src/models/py_adapter_correlator_to_template.py` (domain inference). See [README](./README.md) for current commands.

## Executive Summary

This file is a historical reference for the YAML-fragment composition approach that preceded the current pipeline. The scripts below no longer exist in the repository.

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
