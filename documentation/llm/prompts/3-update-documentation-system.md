---
project_name: CLEAR Docs
title: Documentation System Migration Guide
description: Streamlined instructions for migrating documentation to a target nine_readme_version using Go-based utilities.
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [documentation, migration, system-upgrade, automation, utilities]
---

# Documentation System Migration Guide

A streamlined, executable guide for migrating documentation systems using automated Go utilities. This guide focuses on what needs to change and leverages scripts in `scripts/` to do the heavy lifting.

## Target State Specification

Before starting, define what you're migrating TO.

### Current State
- **Source Version:** nine_readme_version 2.1.1
- **Current Structure:** documentation/ (dev, user, llm, ADRs)
- **Current Metadata Fields:** project_name, title, description, last_updated, nine_readme_version, keywords

### Target State (Fill in below)

```
Project Name:           [DEFINE]
Target Version:         [e.g., 2.2.0]
Folder Structure:       dev, user, llm, ADRs (no changes assumed)
New Metadata Fields:    [List any additions/changes]
Breaking Changes:       [e.g., renamed files, restructured sections]
New Files Required:     [e.g., migration-guide.md, changelog.md]
Link Remappings:        [e.g., docs/old.md → docs/new.md]
```

---

## Responsibilities

**LLM (Automated Tasks):**
- Execute utility scripts (compilation, validation, migration)
- Update file metadata in batch
- Validate structure and links
- Create/move files as needed
- Report results and errors

**Human (Decision Points):**
- Define target specifications (what version, what changes)
- Review pre-migration inventory
- Verify migration results look correct
- Handle link mappings (which old links need updating)
- Commit changes to git
- Monitor for post-migration issues

---

## Phase 1: Preparation

### Step 1: Define Target Specification

Document your migration goals (see Target State Specification above). Be specific about:
- What version are you migrating to?
- What metadata fields are required?
- What folders should exist?
- Are there file renamings or restructuring?
- Are there new files to create?

### Step 2: Create Git Backup

```bash
git tag -a backup-pre-migration-$(date +%Y%m%d) -m "Before documentation migration"
git branch backup-pre-migration-$(date +%Y%m%d)
```

This gives you a recovery point. (No LLM involvement; human-controlled recovery.)

### Step 3: Generate Pre-Migration Inventory

**Build general utilities:**
```bash
cd scripts/general && go build -o doc-utils . && cd ../..
```

**Generate inventory:**
```bash
./scripts/general/doc-utils inventory -docs documentation
```

This shows you:
- Total files to migrate
- Files by category
- Total lines of documentation
- Any non-markdown files to handle

**Validate current state:**
```bash
./scripts/general/doc-utils validate-metadata -docs documentation
./scripts/general/doc-utils validate-links -docs documentation
```

Note any issues before proceeding. Fix or plan to handle them during migration.

---

## Phase 2: Migration

### Step 1: Build Migration Utilities

```bash
cd scripts/migrations && go build -o doc-migrator . && cd ../..
```

### Step 2: Execute Migration

**Basic migration (no link changes):**
```bash
./scripts/migrations/doc-migrator migrate \
  -docs documentation \
  -project "Your Project Name" \
  -target "2.2.0"
```

**Migration with link remappings:**
```bash
./scripts/migrations/doc-migrator migrate \
  -docs documentation \
  -project "Your Project Name" \
  -target "2.2.0" \
  -links "docs/old-pattern.md:docs/new-pattern.md,docs/guide.md:docs/guide.md"
```

**What happens:**
- All markdown files get new metadata headers
- Fields updated to match target version
- Links remapped according to -links flag
- last_updated set to today's date
- All changes written to files (not staged in git)

### Step 3: Handle File Structure Changes

If your target version requires folder reorganization or new files:

**Create new folders:**
```bash
mkdir -p documentation/[new_folder_name]
```

**Create new documentation files:**

Create files manually with proper template:
```yaml
---
project_name: [Your Project]
title: [Document Title]
description: [One-line summary]
last_updated: 2025-12-17
cleardoc_version: [Target Version]
keywords: [tag1, tag2, tag3]
---

# [Document Title]

[Content here]
```

**Move/rename files if needed:**
```bash
mv documentation/old_name.md documentation/new_name.md
```

---

## Phase 3: Validation & Commit

### Step 1: Validate Migration

**Check migration succeeded:**
```bash
./scripts/migrations/doc-migrator validate \
  -docs documentation \
  -project "Your Project Name" \
  -target "2.2.0"
```

This confirms:
- All required folders exist
- All markdown files have required metadata fields
- No missing critical fields

**Run full validation suite:**
```bash
./scripts/general/doc-utils validate-metadata -docs documentation
./scripts/general/doc-utils validate-links -docs documentation
./scripts/general/doc-utils validate-structure -docs documentation
```

**Fix any issues:**
- Broken links: Check link mappings or manually fix references
- Missing metadata: Run utility to update specific fields if needed
- Missing files: Create files using template above

### Step 2: Review Changes

Review changed files to ensure content integrity:

```bash
git diff documentation/ | head -100
```

Spot-check a few files:
- Metadata headers look correct
- Content body unchanged
- Links properly remapped

### Step 3: Commit to Git

```bash
git add documentation/
git commit -m "docs: migrate to version 2.2.0"
```

If issues arise and you need to revert:
```bash
git reset --hard backup-pre-migration-$(date +%Y%m%d)
```

---

## Utility Scripts Reference

### General Utilities (`scripts/general/doc-utils`)

```bash
# Validate all required metadata fields present
./scripts/general/doc-utils validate-metadata -docs documentation

# Find broken links
./scripts/general/doc-utils validate-links -docs documentation

# Check expected folder structure
./scripts/general/doc-utils validate-structure -docs documentation

# Update metadata fields across all docs
./scripts/general/doc-utils update-metadata \
  -docs documentation \
  -project "Project Name" \
  -version "2.1.1"

# Create documentation inventory
./scripts/general/doc-utils inventory -docs documentation
```

See `scripts/README.md` for detailed command documentation.

### Migration Utilities (`scripts/migrations/doc-migrator`)

```bash
# Execute migration to target version
./scripts/migrations/doc-migrator migrate \
  -docs documentation \
  -project "Project Name" \
  -target "2.2.0"

# Validate migration succeeded
./scripts/migrations/doc-migrator validate \
  -docs documentation \
  -project "Project Name" \
  -target "2.2.0"
```

See `scripts/README.md` for detailed command documentation.

---

## Success Criteria

Migration is complete when:

- [ ] Pre-migration inventory created and reviewed
- [ ] Utilities built successfully
- [ ] Migration executed without errors
- [ ] All validation checks pass
- [ ] No broken links remain
- [ ] All metadata fields present
- [ ] Folder structure correct
- [ ] File content unchanged (only headers/links updated)
- [ ] Changes committed to git
- [ ] Git backup tag created (for rollback if needed)

---

## Troubleshooting

### Build fails

**Problem:** `gopkg.in/yaml.v3 not found`

**Solution:**
```bash
cd scripts/general  # or scripts/migrations
go mod download
go build -o doc-utils .  # or doc-migrator
```

### Validation fails: missing metadata fields

**Problem:** Some files missing required fields after migration

**Solution:**
```bash
# Identify which files
grep -L "nine_readme_version:" documentation/**/*.md

# Re-run utility to update missing fields
./scripts/general/doc-utils update-metadata \
  -docs documentation \
  -project "Project Name" \
  -version "2.2.0"
```

### Validation fails: broken links

**Problem:** Broken links found after migration

**Solution:**
Check if link mapping was incomplete. Either:
1. Manually fix links in affected files
2. Re-run migration with additional link mappings
3. Check if files were renamed/moved but not updated in links

```bash
./scripts/general/doc-utils validate-links -docs documentation
```

Shows which files have broken links and which links are broken.

### Need to rollback

**To restore pre-migration state:**
```bash
git reset --hard backup-pre-migration-[DATE]
```

Or from git tag:
```bash
git checkout backup-pre-migration-$(date +%Y%m%d)
```

---

## Best Practices

1. **Always run pre-migration checks** - Identify issues before migration starts
2. **Test link mappings** - If you have complex renamings, test on a sample file first
3. **Commit frequently** - After migration, after validation, after fixes
4. **Keep git backups** - Use git tags/branches, not just filesystem backups
5. **Review diffs** - Spot-check some file diffs to ensure nothing unexpected changed
6. **Document decisions** - Note what link mappings you used, what files were created, etc.

---

## Common Migration Scenarios

### Simple Version Bump (No Structure Changes)

```bash
# Build utilities
cd scripts/general && go build -o doc-utils . && cd ../..
cd scripts/migrations && go build -o doc-migrator . && cd ../..

# Backup
git tag backup-migration

# Migrate
./scripts/migrations/doc-migrator migrate \
  -docs documentation \
  -project "My Project" \
  -target "2.2.0"

# Validate
./scripts/migrations/doc-migrator validate -docs documentation -project "My Project" -target "2.2.0"
./scripts/general/doc-utils validate-links -docs documentation

# Commit
git add documentation/
git commit -m "docs: bump to version 2.2.0"
```

### Migration with File Renamings

```bash
# Before running migration, document link mappings
# Example: docs/dev/architecture.md → docs/dev/system-architecture.md

# Rename files first
mv documentation/dev/architecture.md documentation/dev/system-architecture.md

# Migrate with link mappings
./scripts/migrations/doc-migrator migrate \
  -docs documentation \
  -project "My Project" \
  -target "2.2.0" \
  -links "docs/dev/architecture.md:docs/dev/system-architecture.md"

# Validate
./scripts/migrations/doc-migrator validate -docs documentation -project "My Project" -target "2.2.0"
./scripts/general/doc-utils validate-links -docs documentation

# Commit
git add documentation/
git commit -m "docs: migrate to 2.2.0 and reorganize dev documentation"
```

### Migration with New Files/Folders

```bash
# Backup
git tag backup-migration

# Create new folders
mkdir -p documentation/guides

# Create new files using template
cat > documentation/guides/migration-guide.md << 'EOF'
---
project_name: My Project
title: Migration Guide
description: Guide for migrating from version X to Y
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [migration, guide, changelog]
---

# Migration Guide

[Content here]
EOF

# Migrate existing docs
./scripts/migrations/doc-migrator migrate \
  -docs documentation \
  -project "My Project" \
  -target "2.2.0"

# Validate
./scripts/migrations/doc-migrator validate -docs documentation -project "My Project" -target "2.2.0"
./scripts/general/doc-utils validate-links -docs documentation

# Commit
git add documentation/
git commit -m "docs: migrate to 2.2.0 and add migration guides"
```

---

## Extending the Migration System

### Adding Support for New Version Migrations

See `scripts/README.md` section "Extending Migrations" for detailed steps to add support for migrating between different version pairs (e.g., 2.2.0 → 3.0.0).

### Adding New Validation Utilities

Add new `.go` files to `scripts/general/` with functions that work on documentation paths. Update `main.go` to add CLI command. See `scripts/README.md` for examples.

---

## Summary

This streamlined approach moves heavy lifting to tested, reusable Go utilities:

- **Pre-migration:** Understand what you have (inventory, validation)
- **Migration:** Execute transformation (utilities handle metadata, links, structure)
- **Validation:** Verify success (multiple validators, clear error messages)
- **Recovery:** Git-based rollback always available

**Estimated Time:** 30 minutes for simple version bump, 1-2 hours for complex restructuring

**Key Success Factor:** Define your target state clearly before starting migration.

---

## Next Steps

1. Fill in Target State Specification above
2. Run Phase 1 (Preparation) to understand current documentation
3. Build and test utilities on sample files
4. Execute Phase 2 (Migration)
5. Run Phase 3 validation (Validation & Commit)
6. Review migrated documentation structure
7. Communicate changes to team

---
