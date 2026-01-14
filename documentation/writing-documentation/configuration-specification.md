---
project_name: [PROJECT_NAME]
title: Configuration Specification
description: Rules for documenting system and application configuration files and options.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [configuration, specification, documentation, options, settings]
---

# Configuration Specification

**Path:** Documentation > Writing Documentation > Configuration Specification

Configuration documentation specifies available options, formats, and validation rules for system and application settings.

## Purpose

Configuration documentation:
- Defines all configurable options
- Specifies valid values and constraints
- Explains environment-specific settings
- Documents configuration file formats
- Provides examples for common scenarios

## Structure

Configuration docs are organized by configuration method: environment variables, configuration files, command-line flags, etc.

## Mandatory Sections

### YAML Front Matter

```yaml
---
project_name: [PROJECT_NAME]
title: [SYSTEM] Configuration
description: Complete configuration guide for [SYSTEM].
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [configuration, settings, [SYSTEM], options]
---
```

### Breadcrumb Navigation

```markdown
**Path:** Documentation > Configuration > [SYSTEM] Configuration
```

### Configuration Methods

List how configuration can be provided:

```markdown
## Configuration Methods

Configuration can be provided via:

1. **Environment Variables** - `.env` file or system environment
2. **Configuration File** - `config.yml` or `config.json`
3. **Command-Line Arguments** - Flags passed at startup
4. **Default Values** - Built-in defaults if not specified
```

### Options Reference

Use tables for structured reference:

```markdown
## Options

| Option | Type | Environment | Default | Description |
|--------|------|-------------|---------|-------------|
| `[OPTION_NAME]` | string | `[ENV_VAR]` | `[DEFAULT]` | [DESCRIPTION] |
| `[OPTION_NAME]` | number | `[ENV_VAR]` | `[DEFAULT]` | [DESCRIPTION] |
| `[OPTION_NAME]` | boolean | `[ENV_VAR]` | `[DEFAULT]` | [DESCRIPTION] |
```

Include:
- Option name (as used in configuration files)
- Data type and valid values
- Environment variable name
- Default value
- Constraints or allowed values

## Optional Sections

### Example Configurations

Provide complete example files:

```markdown
## Example Configuration (Development)

```yaml
# config.development.yml
server:
  host: localhost
  port: 3000
  debug: true

database:
  url: postgresql://localhost/[DATABASE_NAME]_dev
  pool_size: 5

logging:
  level: debug
  format: json
```
```

### Validation Rules

```markdown
## Validation

- `[OPTION_NAME]` must be between `[MIN]` and `[MAX]`
- `[OPTION_NAME]` must match pattern `[REGEX]`
- `[OPTION_NAME]` is required when `[OTHER_OPTION]` is enabled
- `[OPTION_NAME]` is incompatible with `[OTHER_OPTION]`
```

### Environment-Specific Configuration

```markdown
## Environment-Specific Settings

### Development

Set `DEBUG=true` and `LOG_LEVEL=debug` for verbose output.

### Production

Set `DEBUG=false` and ensure all secrets are provided via environment variables.
```

## Example

```markdown
---
project_name: [PROJECT_NAME]
title: Application Configuration
description: Configuration options for application startup and operation.
last_updated: 2025-12-20
cleardoc_version: 2.3.0
keywords: [configuration, settings, application, options]
---

# Application Configuration

**Path:** Documentation > Configuration > Application Configuration

Complete reference for application configuration options.

## Configuration Methods

1. **Environment Variables** - `export KEY=value` or `.env` file
2. **Configuration File** - `config.yml` in project root
3. **Command-Line Arguments** - Passed at startup
4. **Defaults** - Built-in values if not specified

## Options Reference

| Option | Type | Environment | Default | Description |
|--------|------|-------------|---------|-------------|
| Port | number | `PORT` | `3000` | Server listening port |
| Host | string | `HOST` | `localhost` | Server bind address |
| Log Level | string | `LOG_LEVEL` | `info` | Logging verbosity: `debug`, `info`, `warn`, `error` |
| Database URL | string | `DATABASE_URL` | required | PostgreSQL connection string |
| Max Connections | number | `DB_MAX_CONN` | `10` | Maximum database connections |
| Cache TTL | number | `CACHE_TTL` | `3600` | Cache expiration in seconds |
| API Key | string | `API_KEY` | required | External API authentication token |
| Debug Mode | boolean | `DEBUG` | `false` | Enable verbose debugging output |

## Example Configuration File

```yaml
# config.yml
server:
  port: 3000
  host: 0.0.0.0
  cors: true

database:
  url: postgresql://user:password@localhost/[DATABASE_NAME]
  max_connections: 10
  pool_timeout: 30

logging:
  level: info
  format: json
  file: ./logs/app.log

cache:
  enabled: true
  ttl: 3600
```

## Environment Variables Example

```bash
# Development
export PORT=3000
export DATABASE_URL=postgresql://localhost/[DATABASE_NAME]_dev
export LOG_LEVEL=debug
export DEBUG=true

# Production
export PORT=8080
export DATABASE_URL=postgresql://prod-server/[DATABASE_NAME]
export LOG_LEVEL=error
export DEBUG=false
```

## Validation Rules

- `PORT` must be between 1024 and 65535
- `LOG_LEVEL` must be one of: `debug`, `info`, `warn`, `error`
- `DATABASE_URL` is required and must be valid PostgreSQL connection string
- `MAX_CONNECTIONS` must be at least 1 and not exceed 100
- `API_KEY` is required when running in production
```

## Size Guidelines

- Total: 400-700 words
- YAML: ~40 words
- Breadcrumb: 5 words
- Configuration Methods: 40-60 words
- Options Reference: 100-150 words (table)
- Examples: 150-300 words
- Validation: 60-100 words
