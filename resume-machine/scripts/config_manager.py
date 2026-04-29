#!/usr/bin/env python3
"""
Configuration manager for resume-machine.
Supports environment variables, config file, and defaults.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration
DEFAULT_CONFIG = {
    'input_dir': 'jobbankjobs',
    'output_dir': 'artifacts',
    'queue_file': 'resume-machine-queue.json',
    'role_templates_dir': 'role-based-templates',
    'unique_data_file': 'resume.unique-data.json',
    'skip_extract': False,
    'dry_run': False,
    'log_level': 'info',
    'pdf_naming_template': 'resume-{candidate}-{company}-{role}.pdf',
    'candidate_name': None,
    'theme': None
}

def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file, environment variables, and defaults.
    
    Priority order:
    1. Environment variables
    2. Config file
    3. Defaults
    """
    config = DEFAULT_CONFIG.copy()
    
    # Load from config file if provided
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                file_config = yaml.safe_load(f) or {}
                config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    # Override with environment variables
    env_prefix = 'RESUME_'
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            config_key = key[len(env_prefix):].lower()
            if config_key in config:
                # Try to convert to appropriate type
                if isinstance(config[config_key], bool):
                    config[config_key] = value.lower() in ('true', '1', 'yes')
                elif isinstance(config[config_key], int):
                    try:
                        config[config_key] = int(value)
                    except ValueError:
                        pass
                else:
                    config[config_key] = value
    
    return config

def get_config_value(key: str, default: Any = None) -> Any:
    """Get a configuration value with fallback to environment variables."""
    # This would be used by the main scripts to get config values
    # For now, we'll just return the default since we're not implementing
    # a global config manager but rather showing how it would work
    return default
