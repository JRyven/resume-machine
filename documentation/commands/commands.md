---
project_name: JSON CV
title: Command Reference
description: All commands for mailToMd - import, tracking, rollback, and debugging
last_updated: 2025-11-07
clear_doc_version: 2.1.0
keywords: [commands, cli, reference, mailToMd]
---

# Command Reference

Complete reference for all mailToMd commands.

---

## Import Commands

### Run Import

```bash
# Standard import
python3 mailToMd.py

# Test mode (uses test config, doesn't modify vault)
python3 mailToMd.py --test

# Custom config
python3 mailToMd.py --config /path/to/custom.config
```

---

## Tracking Commands

### View Statistics

```bash
# Summary of all imports
python3 track_manager.py summary

# Recent imports (last 7 days)
python3 track_manager.py recent --days 7

# List runs available for rollback
python3 track_manager.py list

# Limit results
python3 track_manager.py list --limit 20
```

### Search Files

```bash
# Search tracked files
python3 track_manager.py files --search "subject pattern"

# Limit results
python3 track_manager.py files --limit 50
```

### Cleanup

```bash
# Remove tracking data older than 90 days
python3 track_manager.py cleanup --days 90
```

---

## Rollback Commands

### Basic Rollback

```bash
# Preview rollback (dry run) - shows what would be deleted
python3 track_manager.py rollback --dry-run

# Execute rollback - deletes files from last import
python3 track_manager.py rollback
```

### Rollback Specific Run

```bash
# List runs to find ID
python3 track_manager.py list

# Preview rollback of specific run
python3 track_manager.py rollback --run-id "2025-10-12T04:53:18.987633" --dry-run

# Execute rollback of specific run
python3 track_manager.py rollback --run-id "2025-10-12T04:53:18.987633"
```

---

## Configuration Commands

### Verify Configuration

```bash
# Test configuration loading
python3 -c "
from mailToMd import MailToMdConfig
config = MailToMdConfig()
print(f'Mail dir: {config.mail_dir}')
print(f'Vault: {config.obsidian_vault}')
print(f'Includes: {config.includes}')
"
```

### Test Patterns

```bash
# Test regex pattern matching
python3 -c "
import re
pattern = r'your%40email\.com@imap\.gmail\.com/0-'
mailbox = 'your%40email.com@imap.gmail.com/0-projects.mailbox'
if re.search(pattern, mailbox):
    print('✓ Pattern matches')
else:
    print('✗ No match')
"
```

---

## Testing Commands

### Run Tests

```bash
# Run all tests
python3 tests/test.py
```

### Syntax Check

```bash
# Check Python syntax
python3 -m py_compile mailToMd.py
python3 -m py_compile import_tracker.py
python3 -m py_compile track_manager.py
```

---

## Debugging Commands

### Enable Debug Logging

Edit `mailToMd_python.config`:
```python
MAIL_TO_MD_DEBUG = True
```

### View Logs

```bash
# Tail debug log
tail -f logs/mailToMd_debug_*.log

# Tail error log
tail -f logs/mailToMd_error_*.log

# Search for errors
grep "ERROR" logs/mailToMd_debug_*.log

# View recent entries
tail -n 50 logs/mailToMd_debug_*.log
```

### Test Components

```bash
# Test subject decoding
python3 -c "
from mailToMd import FilenameUtils
subject = '=?UTF-8?q?Test_Subject?='
decoded = FilenameUtils.decode_subject(subject)
print(f'Decoded: {decoded}')
"

# Test destination mapping
python3 -c "
from mailToMd import DestinationMapper
mapper = DestinationMapper()
dest = mapper.find_destination('0-projects.mailbox/subproject.mailbox', '2025-11-07')
print(f'Destination: {dest}')
"
```

---

## Maintenance Commands

### Reset Tracking

```bash
# WARNING: Clears all tracking data - emails will be reprocessed
rm -rf tracking_data/*.json

# Then run import again
python3 mailToMd.py
```

### Count Emails

```bash
# Count .eml files to be processed
find /path/to/mail/dir -name "*.eml" | wc -l
```

### Performance Profiling

```bash
# Profile script execution
python3 -m cProfile -s cumulative mailToMd.py

# Time import run
time python3 mailToMd.py
```

---

## Related Documentation

- [Quick Start](./dev-quick-start.md) - Getting started guide
- [Configuration](./dev-configuration.md) - Configuration options
- [Development Environment](./dev-environment.md) - Setup for contributors
- [Rollback Guide](./dev-rollback-guide.md) - Detailed rollback documentation
