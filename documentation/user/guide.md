---
project_name: JSON Resume
title: User Guide
description: How to use the JSON Resume platform to create, edit, and export professional resumes.
last_updated: 2025-12-18
cleardoc_version: 2.3.0
keywords: [user-guide, resume, json-resume, themes, export]
---

# User Guide


## Overview

This guide walks you through:
- Preparing resume data for dynamic generation
- Previewing your theme in a browser
- Generating a PDF resume
- Running the resume app locally (with or without GitHub authentication)
- Troubleshooting common errors and misconfigurations

## Environments: Node vs Python (.venv)

Some parts of this repository are Node.js based and others are Python-based. Be aware which tools run where:

- Node / JavaScript (no `.venv` required):
	- `pnpm`, `node`, `npm` commands
	- Theme build and preview: `pnpm turbo run build`, `pnpm turbo run dev` (registry preview)
	- PDF export: `resumed` (Node CLI) and `node scripts/preprocess-resume.js`
	- Linking local theme: `npm link` (run from the theme directory)

- Python (`.venv` recommended):
	- Any Python utilities or scripts in the repo (e.g., mailToMd or other Python tooling)
	- Activate the virtual environment before running Python tools:
		```bash
		python3 -m venv .venv
		source .venv/bin/activate
		pip install -r requirements.txt  # if provided
		```

Key point: You do NOT need to activate the Python `.venv` to run Node-based steps such as theme builds or `resumed` PDF export. Only run/activate `.venv` when working with repository Python scripts.

## Core Workflow & Commands


### 1. Prepare Your Resume Data

1. **Edit `resume.source.json`:**
	 - Use variable handles like `{{hiring_company}}`, `{{hiring_position}}`, etc. in your source JSON.
	 - Example:
		 ```json
		 {
			 "basics": {
				 "name": "James Valeil",
				 "label": "{{candidate_title}}",
				 "summary": "Applying for {{hiring_position}} at {{hiring_company}}."
			 },
			 ...
		 }
		 ```
2. **Set default values in `resume.defaults.json`:**
	 - Example:
		 ```json
		 {
			 "hiring_company": "Automattic",
			 "hiring_position": "Senior Engineer",
			 "candidate_title": "Software Engineer"
		 }
		 ```
3. **Do not edit `resume.json` directly.** It is always generated from the source and defaults.

### 2. Preprocess Resume Data

Generate a working `resume.json` by substituting variables:

```bash
node scripts/preprocess-resume.js --hiring_company="Acme Corp" --hiring_position="Software Engineer"
```

This creates `resume.json` with all variables replaced, ready for preview/export. You can override any variable at build time using CLI flags. Always keep `resume.source.json` and `resume.defaults.json` as your source of truth.

### 3. Preview Your Theme Locally

#### Step-by-step:
1. **Install dependencies:**
	```bash
	pnpm install
	```
2. **Build your theme (after any changes):**
	```bash
	pnpm turbo run build --filter=valeii-professional
	```
	- If you see `No package found with name 'valeii-professional' in workspace`, check your theme's `package.json` for the correct name and ensure it's included in your workspace config.
3. **Link your theme globally (required for PDF export):**
	```bash
	cd jsonresume-theme-valeii-professional
	npm link
	cd ..
	```
4. **Start the registry app:**
	```bash
	pnpm turbo run dev --filter=registry
	# or
	pnpm dev --filter=registry
	```
5. **(Optional) Bypass GitHub authentication for local development:**
	```bash
	echo "NEXT_PUBLIC_AUTH_DISABLED=true" > apps/registry/.env
	pnpm turbo run dev --filter=registry
	```
	- This creates a mock user and allows you to preview without logging in.
6. **Open your browser:**
	[http://localhost:3001](http://localhost:3001)

**Note:** Any edits to your theme require a rebuild and browser refresh to see updates.

### 4. Generate PDF Resume

Export your resume to PDF using the `resumed` CLI tool:

```bash
mkdir -p artifacts
resumed export resume.json -t valeii-professional -o artifacts/resume-Company-Position.pdf
```

**Checklist before running:**
- Theme is built and globally linked (`npm link` in theme directory)
- Output directory (`artifacts/`) exists
- `resume.json` is up-to-date (run preprocess if needed)

**Common errors and solutions:**
- `Error: Could not load theme ...` → Run `npm link` in your theme directory
- `No such file or directory, open 'resume.json'` → Run the preprocess step
- `No such file or directory, open 'artifacts/resume-...'` → Create the output directory
- `error: unknown option '-o'` → Use `resumed export`, not `resume-cli export`

**Tip:** You can override any variable at build time using CLI flags (e.g., `--hiring_company`).
Keep `resume.source.json` and `resume.defaults.json` as your source of truth; `resume.json` is always generated and should not be version controlled.

---

## Troubleshooting


## Common Issues & Error Handling

### Workspace & Theme Errors

#### No package found with name 'valeii-professional' in workspace
**Solution:**
- Check your theme's `package.json` for the correct name (should be `valeii-professional`)
- Ensure your workspace config (e.g., `pnpm-workspace.yaml`) includes the theme directory

#### Could not load theme
**Error:** `Error: Could not load theme ./jsonresume-theme-valeii-professional. Is it installed?`
**Solution:**
- Run `npm link` in your theme directory
- Use the theme name (not the path) in the export command

#### No such file or directory for resume.json
**Error:** `ENOENT: no such file or directory, open 'resume.json'`
**Solution:**
- Run the preprocess step to generate `resume.json`
- Use the full absolute path if running from a different directory

#### No such file or directory for output file
**Error:** `ENOENT: no such file or directory, open 'artifacts/resume-...'`
**Solution:**
- Create the output directory: `mkdir -p artifacts`

#### Unknown option '-o' or incorrect command
**Error:** `error: unknown option '-o'`
**Solution:**
- Use `resumed export` (not `resume-cli export`)
- Correct syntax: `resumed export <filename> -t <theme> -o <output>`

### Theme Development Issues

#### Changes not reflecting in PDF
**Solution:**
- Rebuild the theme: `pnpm turbo run build --filter=valeii-professional`
- Relink the theme: `cd jsonresume-theme-valeii-professional && npm link`

#### Preview app blocked by authentication
**Solution:**
- For local development, set the auth bypass environment variable:
	```bash
	echo "NEXT_PUBLIC_AUTH_DISABLED=true" > apps/registry/.env
	pnpm turbo run dev --filter=registry
	```
- This creates a mock user for development without requiring GitHub login

### Preprocessing Issues

#### Variables not substituted
**Solution:**
- Ensure `resume.source.json` uses `{{variable}}` syntax
- Check `resume.defaults.json` for default values
- Run preprocess with overrides: `node scripts/preprocess-resume.js --variable="value"`

---

**Tip:** You can override any variable at build time using CLI flags (e.g., `--hiring_company`).
Keep `resume.source.json` and `resume.defaults.json` as your source of truth; `resume.json` is always generated and should not be version controlled.

---

**Tip:** You can override any variable at build time using CLI flags (e.g., `--hiring_company`).
Keep `resume.source.json` and `resume.defaults.json` as your source of truth; `resume.json` is always generated and should not be version controlled.
