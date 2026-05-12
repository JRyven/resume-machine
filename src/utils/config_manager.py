import yaml
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).parents[2]
_CONFIG_PATH = _PROJECT_ROOT / 'config' / 'config.yaml'

_PATH_KEYS = ('job-listings_dir', 'skills_index_path', 'resume_source_path', 'role_templates_dir')


def load_config() -> dict[str, Any]:
    if not _CONFIG_PATH.exists():
        raise FileNotFoundError(
            f'config.yaml not found at expected path: {_CONFIG_PATH}'
        )
    with open(_CONFIG_PATH) as f:
        cfg = yaml.safe_load(f) or {}

    for key in _PATH_KEYS:
        if key in cfg:
            resolved = (_PROJECT_ROOT / cfg[key]).resolve()
            cfg[key] = str(resolved)

    try:
        from src.utils.logging_manager import get_logger
        get_logger('resume-machine.config').debug('Config loaded: %s', cfg)
    except Exception:
        pass

    return cfg
