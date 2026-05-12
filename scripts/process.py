"""
Batch orchestration CLI for resume-machine.

Usage:
  python scripts/process.py --dir data/job-listings/2026/05/01
  python scripts/process.py --file data/job-listings/2026/05/01/sample.json
  python scripts/process.py --dir ... --dry-run
  python scripts/process.py --file ... --name "Jane Doe"
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is on the path when run as script
_PROJECT_ROOT = Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


def _require_venv() -> None:
    """Abort immediately if not running inside the project .venv."""
    if sys.prefix == sys.base_prefix:
        sys.exit(
            "resume-machine: must run inside the project .venv.\n"
            "  python -m venv .venv\n"
            "  source .venv/bin/activate\n"
            "  pip install -r requirements.txt"
        )
    expected = (_PROJECT_ROOT / '.venv').resolve()
    active   = Path(sys.prefix).resolve()
    if active != expected:
        sys.exit(
            f"resume-machine: wrong virtual environment.\n"
            f"  Expected: {expected}\n"
            f"  Active:   {active}"
        )


from src.utils.logging_manager import get_logger, set_level
from src.utils.config_manager import load_config
from src.data.py_skill_job_correlator import correlate_job

_logger = get_logger('resume-machine.process')


def discover_job_jsons(directory: Path) -> list[Path]:
    """Return all job JSON files in directory (not recursive; excludes correlation and letter files)."""
    return sorted(
        p for p in directory.glob('*.json')
        if '_resume_' not in p.name
        and '_letter_' not in p.name
        and not p.name.startswith('resume-')
        and not p.name.startswith('letter-')
    )


def run(
    job_files: list[Path],
    candidate_name: str | None,
    dry_run: bool,
) -> int:
    import json as _json
    success = 0
    failure = 0
    skipped = 0
    for job_file in job_files:
        try:
            raw = _json.loads(job_file.read_text())
            if raw.get('locked', False):
                _logger.info('Skipping locked job: %s', job_file.name)
                skipped += 1
                continue
            correlate_job(str(job_file), candidate_name=candidate_name, dry_run=dry_run)
            success += 1
        except Exception as exc:
            _logger.error('Failed to process %s: %s', job_file, exc, exc_info=True)
            failure += 1

    _logger.info('Done: %d succeeded, %d skipped, %d failed', success, skipped, failure)
    return 0 if failure == 0 else 1


def main(argv: list[str] | None = None) -> int:
    _require_venv()
    parser = argparse.ArgumentParser(description='Batch-process job JSONs through the correlator')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dir', metavar='DIR', help='Process all job JSONs in this day-level directory')
    group.add_argument('--file', metavar='FILE', help='Process a single job JSON')
    parser.add_argument('--dry-run', action='store_true', help='Print output paths without writing files')
    parser.add_argument('--name', dest='candidate_name', default=None,
                        help='Override candidate name (slugified before use in paths)')
    args = parser.parse_args(argv)

    cfg = load_config()
    set_level(cfg.get('log_level', 'info'))

    if args.dir:
        directory = Path(args.dir).resolve()
        if not directory.is_dir():
            _logger.error('--dir path does not exist: %s', directory)
            return 1
        job_files = discover_job_jsons(directory)
        if not job_files:
            _logger.error('No job JSON files found in: %s', directory)
            return 1
        _logger.info('Processing %d job(s) in %s', len(job_files), directory)
    else:
        job_file = Path(args.file).resolve()
        if not job_file.is_file():
            _logger.error('--file path does not exist: %s', job_file)
            return 1
        job_files = [job_file]

    return run(job_files, args.candidate_name, args.dry_run)


if __name__ == '__main__':
    sys.exit(main())
