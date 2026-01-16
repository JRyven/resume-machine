---
project_name: [PROJECT_NAME]
title: Development Environment
description: Setup guide for developers contributing to [PROJECT_NAME]
last_updated: [YYYY-MM-DD]
clear_doc_version: 2.1.0
status: Active
keywords: [development, setup, environment, contributing, testing]
---

# Development Environment

Setup and guide for developers contributing to [PROJECT_NAME].

---

## Prerequisites

- ***

## Project Structure

```
[PROJECT_NAME]/
├── [PROJECT_NAME].py              # Main script
├── import_tracker.py        # Tracking system
├── track_manager.py         # CLI utility
├── [PROJECT_NAME]_python.config   # Config file
├── [PROJECT_NAME].code-workspace  # VS Code workspace
├── documentation/           # CLEAR Docs structure
├── tests/                   # Test suite
├── logs/                    # Generated logs
├── tracking_data/           # Generated tracking data
└── CLEARDocsV2/            # Documentation framework (reference)
```

---

## Running Tests

See [Command Reference](./dev-commands.md#testing-commands) for all test commands.

```bash
python3 tests/test.py
```

---

## Test Mode

Test without modifying your vault. See [Command Reference](./dev-commands.md#import-commands) for options.

```bash
python3 [PROJECT_NAME].py --test
```

---

## Debug Logging

See [Command Reference](./dev-commands.md#debugging-commands) for debugging workflow.

Enable in `[PROJECT_NAME]_python.config`:

```python
MAIL_TO_MD_DEBUG = True
```

---

## Code Organization

### Main Components

See [Architecture Guide](./architecture.md) for detailed component documentation.

**Key Files:**

1. **[PROJECT_NAME].py** (858 lines)
   - `[PROJECT_NAME]Config` - Configuration
   - `[PROJECT_NAME]Logger` - Logging
   - `EmailProcessor` - Orchestration
   - `EmailContentExtractor` - Content extraction
   - `EmailDateParser` - Date parsing
   - `FilenameUtils` - Filename utilities
   - `DestinationMapper` - Routing

2. **import_tracker.py** (323 lines)
   - `JSONImportTracker` - Tracking system
   - `calculate_file_checksum()` - Duplicate detection

3. **track_manager.py** (375 lines)
   - CLI commands for managing imports

---

## Making Changes

### Adding a New Feature

1. **Check Architecture Guide** - Understand existing design
2. **Review Related Code** - See similar functionality
3. **Write Tests First** - Test-driven development
4. **Implement Feature** - Follow code style
5. **Test Thoroughly** - Run full test suite
6. **Update Documentation** - Keep docs in sync

### Adding a New Destination Rule

Edit `DestinationMapper` in `[PROJECT_NAME].py`:

```python
def _rule_new_mailbox(self, path: str, year: str, month: str) -> Optional[Path]:
    """Handle new-mailbox.mailbox paths."""
    if path.startswith('new-mailbox.mailbox'):
        return Path('new-destination')
    return None
```

Then add to rule chain in `find_destination()`.

---

## Running Specific Components

See [Command Reference](./dev-commands.md#configuration-commands) for component testing commands.

---

## Debugging Tips

See [Command Reference](./dev-commands.md#debugging-commands) for complete debugging workflow including:

- Debug log viewing
- Error log searching
- Pattern testing
- Component testing

---

## Code Style Guide

See [Code Style](./code-style.md) for detailed guidelines.

---

## Common Development Tasks

See [Command Reference](./dev-commands.md) for all commands.

---

## Performance Testing

See [Command Reference](./dev-commands.md#maintenance-commands) for profiling commands.

---

## Contributing Guidelines

1. Read [Architecture Guide](./architecture.md)
2. Follow [Code Style](./code-style.md)
3. Write tests for new features
4. Update documentation
5. Test changes thoroughly

---

## Useful Resources

- [Architecture Guide](./architecture.md) - System design
- [Code Style](./code-style.md) - Coding standards
- [Change Log](./changelog.md) - Version history
- [Command Reference](./dev-commands.md) - All CLI commands
- [ADRs](../ADRs/) - Design decisions

---
