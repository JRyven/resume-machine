---
project_name: [PROJECT_NAME]
title: Troubleshooting Guide
description: Solutions to common problems and issues with [PROJECT_NAME]
last_updated: [YYYY-MM-DD]
clear_doc_version: 2.1.0
status: Active
keywords: [troubleshooting, problems, solutions, help, debug]
---

# Troubleshooting Guide

Solutions to common problems and how to get more information for debugging.

---

## Before You Start

**Always check these first:**

1. **Is Python installed?** Run: `python3 --version`
2. **Is config file present?** Check: `ls [PROJECT_NAME]_python.config`
3. **Are paths correct?** Verify paths exist: `ls /path/to/mail/dir`
4. **Check recent errors?** Look in: `logs/[PROJECT_NAME]_error_*.log`

---

## No Emails Being Imported

### Problem: Script runs but imports nothing

**Check:**

1. **Are INCLUDES patterns correct?**

```bash
# View your patterns
grep "INCLUDES" [PROJECT_NAME]_python.config

# Enable debug to see what's being matched
MAIL_TO_MD_DEBUG = True
python3 [PROJECT_NAME].py
tail logs/[PROJECT_NAME]_debug_*.log
```

2. **Does MAIL_DIR exist?**

```bash
ls -la /path/to/your/mail/dir
```

3. **Are there email files?**

```bash
# Look for .eml files
find /path/to/your/mail/dir -name "*.eml" | head -5
```

4. **Do the patterns match your mailbox names?**

```bash
# List actual mailbox names
ls /path/to/your/mail/dir/*/
```

**Solution:**

Compare your `INCLUDES` patterns against actual mailbox names. URL-encode email addresses (`@` → `%40`).

---

## Wrong Emails Being Imported

### Problem: Emails going to wrong folders

1. **Check the mailbox name** matches destination mapping rules
2. **Verify vault directory structure** exists
3. **Check debug logs** to see routing decisions

```bash
MAIL_TO_MD_DEBUG = True
python3 [PROJECT_NAME].py --test
tail logs/[PROJECT_NAME]_debug_*.log | grep -i "mapping"
```

**Solution:**

See [Configuration Reference](./configuration.md) for destination mapping rules and how to customize routing.

---

## Rollback Issues

### Problem: Can't undo an import

```bash
# Step 1: Preview what would be deleted
python3 track_manager.py rollback --dry-run

# Step 2: Check if files exist
python3 track_manager.py list
```

**If dry-run shows files to delete but they're not being deleted:**

- Check vault path is correct
- Verify files weren't manually deleted already
- Try specifying vault path explicitly:

```bash
python3 track_manager.py rollback \
  --vault-path "/path/to/vault" \
  --dry-run
```

---

## Configuration Problems

### Problem: "Config file not found"

```bash
# Make sure config is in script directory
ls -la [PROJECT_NAME]_python.config

# Or specify custom config
python3 [PROJECT_NAME].py --config /path/to/config.py
```

### Problem: "Invalid configuration"

```bash
# Check Python syntax
python3 -m py_compile [PROJECT_NAME]_python.config

# Look for errors
python3 [PROJECT_NAME].py 2>&1 | head -20
```

**Common syntax errors:**
- Missing quotes around paths
- Unescaped backslashes
- Invalid regex in INCLUDES

---

## Import Performance Issues

### Problem: Import is very slow

1. **Check if scanning too many files:**

```bash
# Count emails being scanned
find /path/to/mail/dir -name "*.eml" | wc -l
```

2. **Refine INCLUDES patterns** to scan fewer mailboxes

3. **Check disk space:**

```bash
df -h /path/to/vault
df -h /path/to/mail/dir
```

**Solution:**

Use more specific include patterns to reduce scanning scope.

---

## Encoding & Character Issues

### Problem: Strange characters in email subjects

This is usually normal - [PROJECT_NAME] handles RFC 2047 encoded subjects. If you see:
- Strange Unicode escape sequences
- Garbled text
- Missing special characters

Check the logs for encoding errors:

```bash
tail logs/[PROJECT_NAME]_error_*.log | grep -i "encod"
```

---

## Duplicate Imports

### Problem: Same emails imported multiple times

This shouldn't happen - the tracking system prevents duplicates. If it does:

1. **Check tracking data integrity:**

```bash
ls -la tracking_data/
cat tracking_data/import_runs.json | python3 -m json.tool | head -50
```

2. **Reset tracking if corrupted:**

```bash
# Warning: This removes all history
rm -rf tracking_data/*.json
python3 [PROJECT_NAME].py
```

---

## Debugging & Getting Help

### Enable Debug Logging

```python
# In [PROJECT_NAME]_python.config
MAIL_TO_MD_DEBUG = True
```

Then run and check logs:

```bash
python3 [PROJECT_NAME].py
tail -f logs/[PROJECT_NAME]_debug_*.log
```

### Check Error Logs

```bash
# View recent errors
tail logs/[PROJECT_NAME]_error_*.log

# Search for specific errors
grep "Error" logs/[PROJECT_NAME]_error_*.log
```

### Test Mode

```bash
# Test with sample emails without modifying vault
python3 [PROJECT_NAME].py --test
```

### View Import History

```bash
# List recent imports
python3 track_manager.py list

# View detailed statistics
python3 track_manager.py summary

# Search for specific emails
python3 track_manager.py files --search "subject"
```

---

## Getting More Help

### Review Documentation

- [Configuration Reference](./configuration.md) - All config options
- [Quick Start](./quick-start.md) - Basic setup
- [Architecture Guide](../dev/architecture.md) - How it works
- [Rollback Guide](./rollback-guide.md) - Undo imports

### Check Project Files

- **Logs**: `logs/[PROJECT_NAME]_debug_*.log`, `logs/[PROJECT_NAME]_error_*.log`
- **Tracking**: `tracking_data/import_runs.json`
- **Config**: `[PROJECT_NAME]_python.config`

### Common Error Messages

**"File not found"**
- Check path exists and is readable

**"Invalid regex in INCLUDES"**
- Check regex syntax in config
- Test patterns: `python3 -c "import re; re.compile(r'pattern')"`

**"Permission denied"**
- Check vault directory permissions
- Check mail directory permissions

---

## When to Rollback

If something goes wrong, it's easy to undo:

```bash
# Preview changes
python3 track_manager.py rollback --dry-run

# Undo the import
python3 track_manager.py rollback

# Fix configuration
vim [PROJECT_NAME]_python.config

# Try again
python3 [PROJECT_NAME].py
```

See [Rollback Guide](./rollback-guide.md) for complete instructions.

---

## Still Having Issues?

1. **Check logs** for specific error messages
2. **Review configuration** against [Configuration Reference](./configuration.md)
3. **Read Architecture** to understand how it works
4. **Try test mode** to verify setup
5. **Reset and retry** after fixing issues
