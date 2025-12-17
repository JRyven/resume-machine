---
project_name: JSON CV
title: Configuration Reference
description: Complete guide to configuring mailToMd with all options and examples
last_updated: 2025-12-17
clear_doc_version: 2.1.0
status: Active
keywords: [configuration, config, settings, mailToMd]
---

# Configuration Reference

Complete guide to configuring mailToMd.

---

## Configuration File Location

mailToMd automatically loads `mailToMd_python.config` from the script directory.

```bash
# Default location
./mailToMd_python.config
```

If you want to use a custom config file:

```bash
python3 mailToMd.py --config /path/to/custom.config
```

---

## Required Settings

### MAIL_DIR

Path to your MailMate mail directory.

```python
MAIL_DIR = "/Users/jamesvaleil/private/MailMate/mail/com.freron.MailMate/Messages.noindex/IMAP"
```

**How to find it:**
1. Open MailMate
2. Go to Preferences
3. Check the Messages location
4. Copy the full path

### OBSIDIAN_VAULT

Path to your Obsidian vault directory.

```python
OBSIDIAN_VAULT = "/Users/jamesvaleil/Library/Mobile Documents/iCloud~md~obsidian/Documents/db"
```

**How to find it:**
1. Open Obsidian
2. Go to Settings → About
3. Look for "Vault location"
4. Copy the path

### INCLUDES

List of mailbox patterns to include (Python regex syntax).

```python
INCLUDES = [
    r"jryven%40gmail\.com@imap\.gmail\.com/0-\.mailbox",           # All 0-projects
    r"jryven%40gmail\.com@imap\.gmail\.com/1-calendar\.mailbox",   # Calendar
    r"jryven%40gmail\.com@imap\.gmail\.com/5-read\.mailbox",       # Reading list
]
```

Only emails in mailboxes matching these patterns will be imported.

**Pattern Matching Tips:**
- Use `\.` to escape dots
- Use `%40` for `@` in email addresses
- Use regex `.*` for wildcard matching
- Use `^` and `$` to match start/end

---

## Optional Settings

### MAIL_TO_MD_DEBUG

Enable debug logging for troubleshooting.

```python
MAIL_TO_MD_DEBUG = True    # Enable debug logging
MAIL_TO_MD_DEBUG = False   # Disable (default)
```

When enabled, detailed debug information is written to `logs/mailToMd_debug_*.log`.

---

## Understanding Mailbox Paths

### Email Address URL Encoding

In MailMate paths, email addresses are URL-encoded:
- `@` becomes `%40`
- `.` stays as `.` (dots are fine)

**Example:**
```
jryven@gmail.com  →  jryven%40gmail.com
```

### Mailbox Naming

Mailboxes appear as `.mailbox` folders:

```
IMAP/
├── jryven%40gmail.com@imap.gmail.com/
│   ├── 0-projects.mailbox/
│   ├── 1-calendar.mailbox/
│   ├── 1-journal.mailbox/
│   ├── 2-art.mailbox/
│   ├── 5-read.mailbox/
│   └── ...
```

### Nested Mailboxes

Nested mailboxes use `/` path separators:

```
0-projects.mailbox/
├── subproject1.mailbox/
│   └── Messages/
└── subproject2.mailbox/
    └── Messages/
```

Pattern: `0-projects\.mailbox/subproject.*\.mailbox`

---

## Destination Mapping

The tool automatically maps mailboxes to vault directories using intelligent rules.

### Mapping Rules (In Priority Order)

#### 1. Projects (0-{name}.mailbox)

Mailbox: `0-projects.mailbox/subproject.mailbox`
Destination: `0-projects/subproject/`

#### 2. Calendar (1-calendar.mailbox)

Mailbox: `1-calendar.mailbox`
Destination: `1-calendar/events/`

#### 3. Journal (1-journal.mailbox)

Mailbox: `1-journal.mailbox`
Destination: `1-journal/entries/{year}/{month}/`

#### 4. Knowledge Base (3-know.mailbox)

Mailbox: `3-know.mailbox/topic.mailbox`
Destination: `3-know/topic/`

#### 5. Places (5-place.mailbox)

Mailbox: `5-place.mailbox/location.mailbox`
Destination: `5-place/location/`

#### 6. People (7-people.mailbox)

Mailbox: `7-people.mailbox`
Destination: `7-people/`

#### 7. Dated Categories

These mailboxes create `{year}/{month}/` subdirectories:

- `2-art.mailbox` → `2-art/{year}/{month}/`
- `2-write.mailbox` → `2-write/{year}/{month}/`
- `5-read.mailbox` → `5-read/{year}/{month}/`
- `5-watch.mailbox` → `5-watch/{year}/{month}/`
- `6-career.mailbox` → `6-career/{year}/{month}/`
- `6-home-operations.mailbox` → `6-home-operations/{year}/{month}/`

#### 8. Default Fallback

Any mailbox not matching above rules:

Destination: `{mailbox_name}/{year}/{month}/`

---

## Configuration Examples

### Minimal Configuration

Import all emails from one mailbox:

```python
MAIL_DIR = "/Users/you/private/MailMate/mail/com.freron.MailMate/Messages.noindex/IMAP"
OBSIDIAN_VAULT = "/Users/you/Documents/vault"

INCLUDES = [
    r"your_email%40gmail\.com@imap\.gmail\.com/.*",  # All mailboxes
]

MAIL_TO_MD_DEBUG = False
```

### Project-Focused Configuration

Import only project and calendar emails:

```python
MAIL_DIR = "/Users/you/private/MailMate/mail/com.freron.MailMate/Messages.noindex/IMAP"
OBSIDIAN_VAULT = "/Users/you/Documents/vault"

INCLUDES = [
    r"your_email%40gmail\.com@imap\.gmail\.com/0-",        # All projects
    r"your_email%40gmail\.com@imap\.gmail\.com/1-calendar", # Calendar only
]

MAIL_TO_MD_DEBUG = False
```

### Multiple Accounts

Import from multiple email accounts:

```python
INCLUDES = [
    r"account1%40gmail\.com@imap\.gmail\.com/0-.*",
    r"account2%40gmail\.com@imap\.gmail\.com/0-.*",
    r"account3%40gmail\.com@imap\.gmail\.com/5-read",
]
```

---

## Troubleshooting Configuration

### No emails being imported

1. Check `INCLUDES` patterns are correct
2. Verify `MAIL_DIR` path exists
3. Enable debug logging to see what's being scanned
4. Check log file for pattern matching details

### Emails going to wrong directory

1. Check mailbox name matches expected pattern
2. Review destination mapping rules above
3. Enable debug logging to see path decisions
4. Check vault directory structure is correct

### Configuration file not loading

1. Ensure `mailToMd_python.config` is in same directory as script
2. Check file syntax (valid Python)
3. Look for error messages in console output

---

## Advanced Configuration

### Custom Test Configuration

Create `mailToMdTest.config` for test mode:

```python
MAIL_DIR = "/path/to/test/emails"
OBSIDIAN_VAULT = "/path/to/test/vault"
INCLUDES = [r"test\.mailbox"]
MAIL_TO_MD_DEBUG = True
```

Then run: `python3 mailToMd.py --test`

---

## Configuration Validation

To verify your configuration, see [Command Reference](./dev-commands.md#configuration-commands) for testing commands.

---

## See Also

- [Quick Start](./dev-quick-start.md) - Getting started
- [Command Reference](./dev-commands.md) - All CLI commands
- [Architecture Guide](./architecture.md) - How configuration is used

---

**Last Updated**: 2025-11-07
