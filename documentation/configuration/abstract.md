# Configuration System

Professional, environment-aware configuration management for multi-environment deployments.

## Executive Summary

The configuration system provides centralized, environment-aware settings orchestration through a single source of truth. It enables seamless switching between development, staging, and production environments without code changes, centralizes path management, and supports both programmatic and CLI-based configuration loading. The system follows a separation-of-concerns pattern where each configuration file handles a specific domain (database, API, etc.) while the orchestrator routes environment-specific variants.

## Best Practices Checklist

- ✓ Use environment variables for sensitive data (`APP_ENV`, `DATABASE_PASSWORD`, etc.)
- ✓ Never commit production credentials; use placeholders in templates
- ✓ Define all expected placeholders with `[PLACEHOLDER_NAME]` syntax in templates
- ✓ Test configuration loading in CI/CD before deployment
- ✓ Validate required config keys exist before application startup
- ✓ Document environment-specific differences between develop and production configs
- ✓ Use consistent file naming across environments (database.yaml, api.yaml, etc.)

## Table of Contents

1. **Architecture Overview** - How the configuration system organizes environment routing and file hierarchy
2. **File Structure** - Directory layout and naming conventions for config files
3. **Core Concepts** - Environment orchestration, routing, and setting precedence
4. **Implementation Guide** - Setting up configuration for your application
5. **Usage Patterns** - Common patterns for accessing and loading configurations
6. **Example Scenarios** - Real-world deployment configurations

## Quick Links

### Essential Commands

```bash
# Set environment (command line)
export APP_ENV=production

# Override in app.yaml
environment: "develop"  # or "production"

# Load config files in Python
python -c "from config_loader import ConfigLoader; c = ConfigLoader(); print(c.environment)"
```

## Getting Started

### New to the Project

1. **Read the [Architecture Overview](#architecture-overview)** - Understand how environments are routed through the orchestrator
2. **Review the [File Structure](#file-structure)** - See how config files are organized by environment and domain
3. **Examine the [Core Concepts](#core-concepts)** - Learn environment variables, routing, and setting precedence
4. **Study the [Example Scenarios](#example-scenarios)** - See realistic develop and production configurations
5. **Follow the [Implementation Guide](#implementation-guide)** - Set up configuration for your specific application
6. **Test with [Usage Patterns](#usage-patterns)** - Verify configuration loading works correctly

### Quick Start Checklist

- [ ] Copy `app-template.yaml` to `app.yaml` and update `[PLACEHOLDER]` values
- [ ] Copy environment-specific templates (e.g., `database-template.yaml`) to actual config files
- [ ] Replace all `[PLACEHOLDER]` markers with your actual values
- [ ] Set `APP_ENV` environment variable or update `environment` in `app.yaml`
- [ ] Test configuration loading: `python config_loader_example.py`
- [ ] Verify all required config files are referenced and accessible

## Architecture Overview

**`app.yaml`** serves as the central orchestrator that:

1. **Defines active environment** - Single location to specify `develop` or `production`
2. **Routes configuration files** - Maps config domains to environment-specific files
3. **Provides environment paths** - Centralized directory management (data, logs, output)
4. **Applies common settings** - Default values shared across all environments
5. **Supports environment override** - `APP_ENV` variable overrides file setting

### Design Benefits

- **Single source of truth** - Environment selection in one location prevents inconsistency
- **Prevents configuration errors** - Accidental production code runs with wrong configs
- **Centralizes path management** - No hardcoded paths scattered through codebase
- **Easy environment switching** - One line change or environment variable
- **Separation of concerns** - Each config file handles specific domain/responsibility

## File Structure

```
config/
├── app.yaml                          # Main orchestrator (environment-aware)
├── app-template.yaml                 # Template for initial setup
│
├── develop/
│   ├── database.yaml                 # Database config for development
│   ├── database-template.yaml        # Template with placeholders
│   ├── api.yaml                      # API config for development
│   └── api-template.yaml             # Template with placeholders
│
├── production/
│   ├── database.yaml                 # Database config for production
│   ├── database-template.yaml        # Template with placeholders
│   ├── api.yaml                      # API config for production
│   └── api-template.yaml             # Template with placeholders
│
└── config_loader_example.py          # Python implementation example
```

### Naming Conventions

- **Orchestrator**: `app.yaml` (remove `-template` suffix after customization)
- **Domain-specific configs**: Use descriptive names (`database.yaml`, `api.yaml`, not `setting1.yaml`)
- **Templates**: Keep `-template.yaml` suffix to indicate files need customization
- **Environment folders**: Use exact names `develop/` and `production/`

## Core Concepts

### 1. Environment Selection

The system determines active environment through priority order:

1. **Environment variable** (highest priority): `export APP_ENV=production`
2. **Configuration file**: `environment: "production"` in `app.yaml`
3. **Default**: `develop` (if neither above is set)

```yaml
# In app.yaml
environment: 'develop' # Used if APP_ENV not set
```

```bash
# Override via environment variable (takes precedence)
export APP_ENV=production
```

### 2. Configuration Routing

The `environments` section maps each environment to its config files:

```yaml
environments:
  develop:
    config_files:
      database: config/develop/database.yaml
      api: config/develop/api.yaml
    paths:
      data: data-develop
      logs: logs-develop

  production:
    config_files:
      database: config/production/database.yaml
      api: config/production/api.yaml
    paths:
      data: data
      logs: logs
```

### 3. Common Settings

Settings in the `common` section apply to all environments:

```yaml
common:
  app_name: '[PROJECT_NAME]'
  version: '1.0.0'
  logging:
    format: 'json'
```

### 4. Setting Precedence

When accessing configuration, precedence is:

1. **Environment-specific settings** (highest priority)
2. **Common settings** (if not in environment-specific)
3. **Defaults in application code** (if not in config)

## Implementation Guide

### Step 1: Set Up Template Files

```bash
# Copy main orchestrator template
cp config/app-template.yaml config/app.yaml

# Copy environment-specific templates
cp config/develop/database-template.yaml config/develop/database.yaml
cp config/develop/api-template.yaml config/develop/api.yaml
cp config/production/database-template.yaml config/production/database.yaml
cp config/production/api-template.yaml config/production/api.yaml
```

### Step 2: Replace Placeholders

Replace all `[PLACEHOLDER]` markers with actual values:

```yaml
# Before
host: "[DATABASE_HOST]"
port: "[DATABASE_PORT]"

# After
host: "localhost"
port: 5432
```

### Step 3: Use in Application

**Python Example:**

```python
from config_loader import ConfigLoader

config = ConfigLoader("config/app.yaml")

# Get environment-specific config
database_config = config.load_additional_config('database')

# Access paths
paths = config.get_paths()
print(f"Data directory: {paths['data']}")

# Check environment
if config.is_production():
    # Production-specific logic
    enable_ssl()
```

### Step 4: Environment Setup

```bash
# Development
export APP_ENV=develop
python app.py

# Production
export APP_ENV=production
python app.py
```

## Usage Patterns

### Loading Configuration in Code

```python
# Initialize loader
config = ConfigLoader("config/app.yaml")

# Get current environment
print(config.environment)  # Output: "develop" or "production"

# Load domain-specific config
db_config = config.load_additional_config('database')
api_config = config.load_additional_config('api')

# Get paths for current environment
paths = config.get_paths()
log_dir = paths['logs']

# Get common settings
app_name = config.get_common_config('app_name')
```

### Validating Configuration

```python
# Check required config keys
required_keys = ['database', 'api', 'paths']
config_files = config.get_config_files()

for key in required_keys:
    if key not in config_files:
        raise ValueError(f"Missing required config: {key}")
```

### Using with Sensitive Data

Always use environment variables for secrets:

```bash
# Set sensitive values via environment
export DATABASE_PASSWORD="[your-password]"
export API_SECRET_KEY="[your-secret]"
```

```yaml
# Reference in config (don't embed directly)
database:
  password: '[DATABASE_PASSWORD]' # Replaced at runtime
```

## Example Scenarios

### Development Configuration

```yaml
# app.yaml
environment: 'develop'

# Uses: config/develop/database.yaml, config/develop/api.yaml
# Paths: data-develop/, logs-develop/
# Debug mode: enabled
# Log level: DEBUG
```

**Development characteristics:**

- Debug mode enabled for troubleshooting
- Verbose logging for detailed trace
- Relaxed security settings for ease of testing
- High database connection limits for testing
- Low rate limits to simulate edge cases

### Production Deployment

```yaml
# app.yaml
environment: 'production'
# OR: export APP_ENV=production

# Uses: config/production/database.yaml, config/production/api.yaml
# Paths: data/, logs/
# Debug mode: disabled
# Log level: INFO
```

**Production characteristics:**

- Debug mode disabled for performance
- Minimal logging (INFO level only)
- Strict security settings (SSL required, secure JWT tokens)
- Conservative database connection limits
- Strict rate limiting for API protection

### CI/CD Pipeline

```bash
# Run tests with develop config
export APP_ENV=develop
npm test

# Run with production config before deployment
export APP_ENV=production
npm run validate-config
npm run smoke-test
```

## Related Documentation

- [Development Guide](./dev-abstract.md) - Overall development practices
- [Error Handling](./error-handling-abstract.md) - Handling configuration errors
- [Deployment Guide](./deployment-abstract.md) - Deploying with proper environment configuration
- [Documentation Management](./documentation-management.md) - Documenting environment-specific behavior
- [CLEAR Docs Setup](../../setup/CLEAR-Docs-setup-guide.md) - Project initialization
