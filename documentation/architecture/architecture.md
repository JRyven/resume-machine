---
project_name: [PROJECT_NAME]
title: Architecture Overview
description: System architecture, design patterns, layer structure, and architectural principles.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [architecture, design-patterns, layers, principles]
---

# Architecture Guide

[PROJECT_NAME] system design and component architecture.

---

## System Overview

[PROJECT_NAME] processes email files (`.eml` format) from MailMate and converts them to Markdown for Obsidian vaults.

### Processing Pipeline

```
MailMate Directory (.eml files)
       ↓
[Configuration & Filtering]
       ↓
[Email Processing Pipeline]
  ├─ Metadata extraction
  ├─ Content extraction (HTML→MD)
  ├─ Tag generation
  ├─ Date filtering
  └─ Hashtag/cleanup pattern removal
       ↓
[Destination Mapping]
       ↓
[Markdown Generation]
       ↓
[Import Tracking]
       ↓
Obsidian Vault (Markdown files)
```

---

## Core Components

### 1. Configuration Management (`[PROJECT_NAME]Config`)

**Responsibility:** Load and manage configuration settings

**Key Methods:**

- `__init__()` - Initialize with defaults, auto-load `[PROJECT_NAME]_python.config`
- `_load_config()` - Parse Python config file
- `_load_test_config()` - Load test configuration

**Design Pattern:** Single Responsibility

- Only handles configuration
- Loads defaults first, then overrides
- Separates test config from production

---

### 2. Email Processing (`EmailProcessor`)

**Responsibility:** Orchestrate complete email-to-markdown conversion

**Key Methods:**

- `process_mailbox()` - Main processing loop
- `_create_markdown_file()` - Write markdown to vault
- `_should_process_file()` - Determine if email should be processed

**Design Pattern:** Facade

- Coordinates other components
- Hides complexity of email processing

---

### 3. Email Content Extraction (`EmailContentExtractor`)

**Responsibility:** Extract and clean email content

**Key Methods:**

- `extract()` - Get clean email body
- `_extract_text_part()` - Handle text/plain parts
- `_extract_html_part()` - Handle HTML parts with conversion
- `_html_to_markdown()` - Convert HTML to Markdown (uses SimpleHTMLToMarkdown)
- `_try_decode_base64()` - Detect and decode base64 content
- `_is_base64_gibberish()` - Identify structured content (calendar invitations)

**Features:**

- Three-level fallback: text/plain → HTML converted → get_body()
- HTML-to-Markdown conversion via SimpleHTMLToMarkdown class (203 lines, zero dependencies)
- Removes quoted text (email replies)
- Handles forwarding headers
- Detects and decodes base64 content
- Preserves paragraph structure
- Limits content to 3000 characters

**Design Pattern:** Single Responsibility - Only handles content extraction

---

### 3a. HTML to Markdown Conversion (`SimpleHTMLToMarkdown`)

**Responsibility:** Convert HTML email bodies to clean Markdown

**Implementation:** HTMLParser-based converter (203 lines)

**Supported Tags:**

- Blocks: p, br, h1-h6, blockquote, pre
- Inline: strong, em, code, a
- Lists: ul, ol, li

**Features:**

- Standard library only (no external dependencies)
- Block vs inline state machine
- List nesting support
- URL extraction from links
- HTML entity unescaping

---

### 4. Tag Generation (`TagGenerator`)

**Responsibility:** Generate YAML frontmatter tags from email metadata

**Implementation:** 145+ lines with three extraction methods

**Key Methods:**

- `extract_mailbox_tags()` - Tags from mailbox hierarchy (e.g., "projects", "career")
- `extract_sender_tags()` - Tags from sender with fallback (name → email → domain)
- `extract_topic_tags()` - Tags from common email patterns (invoice, newsletter, notification)
- `generate_tags()` - Orchestrates all extraction methods

**Features:**

- Multi-source tag generation
- Graceful fallback for missing sender names
- Topic detection via regex patterns
- Deduplication and sanitization
- Conditional frontmatter (only adds if tags generated)

---

### 5. Email Date Parsing (`EmailDateParser`)

**Responsibility:** Parse and format email dates

**Key Methods:**

- `parse()` - Parse date string in various formats
- Handles null values gracefully

**Features:**

- RFC 2822 format support
- ISO format parsing
- Multiple format fallbacks
- Null safety

---

### 6. Filename Generation (`FilenameUtils`)

**Responsibility:** Generate safe, readable filenames

**Key Methods:**

- `decode_subject()` - Decode RFC 2047 subjects with cleanup patterns
- `_apply_cleanup_patterns()` - Apply SUBJECT_CLEANUP_PATTERNS regex
- `_remove_hashtags()` - Strip hashtags (literal #, HTML &#35;, URL %23)
- `sanitize_filename()` - Make filesystem-safe filenames
- `generate()` - Create complete filename with date prefix

**Features:**

- Multi-stage cleaning: decode → cleanup patterns → hashtag removal → sanitize
- Configurable cleanup patterns via SUBJECT_CLEANUP_PATTERNS
- Handles encoded subjects, hashtags, list tags, tracking codes
- Date-prefixed filenames for sorting

---

### 7. Destination Mapping (`DestinationMapper`)

**Responsibility:** Route emails to appropriate vault directories

**Rule-Based Architecture:** Evaluates destination rules in priority order

**Key Methods:**

- `find_destination()` - Determine target directory
- Rule methods:
  - `_rule_projects()` - 0-projects.mailbox routing
  - `_rule_calendar()` - 1-calendar.mailbox → events/
  - `_rule_journal()` - 1-journal.mailbox → entries/YYYY/MM/
  - `_rule_dated_categories()` - Date-based organization for read, career, art, etc.
  - `_rule_nested_mailboxes()` - Handle mailbox hierarchies
  - `_rule_fallback()` - Default routing

**Features:**

- Priority-ordered rule evaluation
- Date-based categorization for specific mailboxes
- Nested mailbox support
- Configurable via rules
- Extensible for new routing logic

---

### 8. Import Tracking (`JSONImportTracker`)

- `_rule_calendar()` - 1-calendar.mailbox
- `_rule_journal()` - 1-journal.mailbox
- `_rule_knowledge()` - 3-know.mailbox
- `_rule_places()` - 5-place.mailbox
- `_rule_people()` - 7-people.mailbox
- `_rule_dated_categories()` - 2-art, 5-read, 6-career, etc.
- `_rule_fallback()` - Default routing

**Design Pattern:** Strategy Pattern (Rule Chain)

- Each rule is independent
- Rules applied in priority order
- Extensible for new routing rules

---

### 7. Import Tracking (`JSONImportTracker`)

**Responsibility:** Track all imports and prevent duplicates

**Key Data:**

- `import_runs.json` - Complete run history
- `files_index.json` - Per-file processing records
- `summary_stats.json` - Summary statistics

**Key Methods:**

- `start_run()` - Begin new import run
- `record_file()` - Track individual file processing
- `end_run()` - Complete import run
- `is_duplicate()` - Check if file already processed
- `calculate_file_checksum()` - Detect unchanged files

**Features:**

- Duplicate prevention via checksum + mod time
- Detailed audit trail
- Per-run statistics
- Searchable file index

**Design Pattern:** Repository Pattern

- Encapsulates data persistence
- Separates data storage from business logic

---

### 8. Logging (`[PROJECT_NAME]Logger`)

**Responsibility:** Centralized logging setup

**Features:**

- Separate debug and error logs
- Rolling file handler (10MB per file, 5 backups)
- Configurable via `MAIL_TO_MD_DEBUG`
- Timestamps and level indicators

---

## Data Flow

### Import Process

```
1. Configuration Load
   ├─ Load [PROJECT_NAME]_python.config
   ├─ Apply defaults
   └─ Validate settings

2. Mailbox Scanning
   ├─ Find .eml files in MAIL_DIR
   ├─ Apply INCLUDES filter patterns
   └─ Build file list

3. For Each Email:
   ├─ Check if already processed (duplicate prevention)
   ├─ Extract metadata
   │  ├─ Subject (decode RFC 2047)
   │  ├─ From/To addresses
   │  ├─ Date (parse multiple formats)
   │  └─ Message ID
   ├─ Extract content
   │  ├─ Get text/html parts
   │  ├─ Remove quotes/forwards
   │  ├─ Detect and decode base64
   │  └─ Limit to 3000 chars
   ├─ Generate filename
   │  ├─ Decode subject
   │  ├─ Sanitize for filesystem
   │  └─ Add date prefix
   ├─ Map destination
   │  ├─ Evaluate mapping rules
   │  └─ Determine target directory
   ├─ Create markdown file
   │  ├─ Write YAML frontmatter
   │  ├─ Write content
   │  └─ Get file path
   └─ Record in tracking system
      ├─ Track success/failure
      ├─ Store file metadata
      └─ Update statistics

4. Finalize Run
   ├─ Calculate statistics
   ├─ Write tracking data
   └─ Print summary
```

---

## Design Principles Applied

### Single Responsibility Principle

Each class has one reason to change:

- `EmailContentExtractor` - Only changes if content extraction logic changes
- `DestinationMapper` - Only changes if routing rules change
- `JSONImportTracker` - Only changes if data persistence changes

### Open/Closed Principle

System is open for extension, closed for modification:

- New destination rules can be added without modifying existing rules
- New file types could be processed by adding to pipeline
- Logging system can be enhanced without modifying core logic

### Dependency Inversion

Components depend on abstractions, not concretions:

- `EmailProcessor` depends on abstract components, not implementations
- Logger uses standard `logging` module abstraction
- Configuration object provides interface to settings

### Interface Segregation

Components don't depend on unused interfaces:

- `EmailContentExtractor` only exposes content extraction methods
- `DestinationMapper` only exposes destination finding
- Each component has focused, minimal interface

---

## Key Files

```
[PROJECT_NAME]/
├── [PROJECT_NAME].py              # Main script (1380 lines)
│   ├─ SimpleHTMLToMarkdown  # HTML to Markdown converter (203 lines)
│   ├─ [PROJECT_NAME]Config        # Configuration management
│   ├─ [PROJECT_NAME]Logger        # Logging setup
│   ├─ EmailProcessor        # Orchestrator
│   ├─ EmailContentExtractor # Content extraction
│   ├─ TagGenerator          # YAML tag generation (145 lines)
│   ├─ EmailDateParser       # Date parsing
│   ├─ FilenameUtils         # Filename generation with cleanup
│   └─ DestinationMapper     # Routing logic
│
├── import_tracker.py        # Import tracking (323 lines)
│   └─ JSONImportTracker     # Tracking system
│
├── track_manager.py         # CLI utility (375 lines)
│   └─ Command handlers
│
├── [PROJECT_NAME]_python.config   # Configuration with SUBJECT_CLEANUP_PATTERNS, IMPORT_CUTOFF_DATE
├── logs/                    # Log directory
├── tracking_data/           # Import history
└── tests/                   # Test suite
```

---

## Error Handling Strategy

**Graceful Degradation:**

- Email processing continues even if individual emails fail
- Invalid dates fall back to current date
- Encoding errors produce readable approximation
- Missing content fields are handled with defaults

**Logging & Reporting:**

- All errors logged with context
- Summary reports success/failure counts
- Detailed logs available in debug mode

---

## Performance Characteristics

- **Scanning**: Linear in number of `.eml` files
- **Processing**: Linear in content size
- **Tracking**: O(1) lookup for duplicates (file checksum)
- **Memory**: Streaming - doesn't load entire mailbox
- **Typical Speed**: 100-500 emails/minute depending on size

---

## Security Considerations

- Reads from local MailMate directory only
- Writes to local Obsidian vault only
- No network access
- Configuration file in plain Python (review before running)
- Logs may contain email metadata (keep secure)

---

## Extensibility Points

### Add New Destination Rule

In `DestinationMapper.find_destination()`, add to rule list:

```python
def _rule_custom_mailbox(self, path: str, year: str, month: str) -> Optional[Path]:
    if re.match(r'^custom\.mailbox', path):
        return Path('custom-folder')
    return None
```

### Add New Content Processor

Extend `EmailContentExtractor` to handle new formats:

```python
def _extract_custom_format(self, msg):
    # Custom extraction logic
    pass
```

### Integrate Different Email Format

Create adapter for new email format (not just `.eml`):

```python
class CustomEmailReader:
    def read(self, path):
        # Convert to email.Message object
        pass
```

---

## Testing Strategy

Located in `tests/test.py`:

- Subject decoding tests
- Base64 content detection tests
- Complete email processing tests

Run with: `python3 tests/test.py`

---

## See Also

- [Rollback Guide](../user/rollback-guide.md) - How rollback works
- [ADRs](../ADRs/) - Architectural decisions
- [Configuration](../user/configuration.md) - Configuration options

---

**Last Updated**: November 6, 2025
