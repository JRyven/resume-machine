"""
Local HTTP server for resume-machine UX.

Endpoints:
  GET /                              → serves src/api/resume-machine.html
  GET /api/years                     → JSON array of year strings, sorted descending
  GET /api/jobs?year=YYYY[&month=MM] → JSON array of job summaries
  GET /api/resume                    → JSON content of data/resume.source.json
  GET /api/correlation?path=...      → merged correlation + letter JSON

Usage: python -m src.api.serve [--port 8080]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

_PROJECT_ROOT = Path(__file__).parents[2]
_HTML_FILE = Path(__file__).parent / 'resume-machine.html'


def _require_venv() -> None:
    """Abort immediately if not running inside a virtual environment."""
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


# Deferred import to allow module load without config
_config: dict | None = None


def _get_config() -> dict:
    global _config
    if _config is None:
        from src.utils.config_manager import load_config
        _config = load_config()
    return _config


def _json_response(handler, data, status: int = 200) -> None:
    body = json.dumps(data, indent=2).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.end_headers()
    handler.wfile.write(body)


def _error(handler, status: int, message: str) -> None:
    _json_response(handler, {'error': message}, status)


def _api_years(handler) -> None:
    cfg = _get_config()
    base = Path(cfg['job-listings_dir'])
    if not base.is_dir():
        _json_response(handler, [])
        return
    years = sorted(
        [d.name for d in base.iterdir() if d.is_dir() and d.name.isdigit()],
        reverse=True,
    )
    _json_response(handler, years)


def _api_jobs(handler, params: dict) -> None:
    cfg = _get_config()
    base = Path(cfg['job-listings_dir'])

    year = params.get('year', [None])[0]
    month = params.get('month', [None])[0]

    if not year:
        _error(handler, 400, 'year parameter required')
        return

    search_root = base / year
    if month:
        search_root = search_root / f'{int(month):02d}'

    if not search_root.is_dir():
        _json_response(handler, [])
        return

    jobs: list[dict] = []
    for corr_file in sorted(search_root.rglob('resume-*.json'), reverse=True):
        try:
            with open(corr_file) as f:
                data = json.load(f)
            meta = data.get('metadata', {})
            rel = str(corr_file.relative_to(_PROJECT_ROOT))
            jobs.append({
                'path': rel,
                'job_title': meta.get('job_title', ''),
                'employer': meta.get('employer', ''),
                'location': meta.get('location', ''),
                'domain': data.get('domain', ''),
            })
        except Exception:
            pass

    _json_response(handler, jobs)


def _api_resume(handler) -> None:
    cfg = _get_config()
    resume_path = Path(cfg['resume_source_path'])
    if not resume_path.is_file():
        _error(handler, 404, 'resume.source.json not found')
        return
    try:
        with open(resume_path) as f:
            data = json.load(f)
        _json_response(handler, data)
    except Exception as exc:
        _error(handler, 500, str(exc))


def _api_correlation(handler, params: dict) -> None:
    cfg = _get_config()
    path_param = params.get('path', [None])[0]
    if not path_param:
        _error(handler, 400, 'path parameter required')
        return

    # Path-traversal guard: resolve and confirm it lives under job-listings_dir
    try:
        abs_path = (_PROJECT_ROOT / path_param).resolve()
        base_resolved = Path(cfg['job-listings_dir']).resolve()
        abs_path.relative_to(base_resolved)   # raises ValueError if outside
    except ValueError:
        _error(handler, 400, 'path is outside permitted directory')
        return
    except Exception as exc:
        _error(handler, 400, f'invalid path: {exc}')
        return

    if not abs_path.is_file():
        _error(handler, 404, f'correlation file not found: {path_param}')
        return

    try:
        with open(abs_path) as f:
            data = json.load(f)
    except Exception as exc:
        _error(handler, 500, f'failed to read correlation file: {exc}')
        return

    # Merge companion letter JSON if present
    letter_name = abs_path.name.replace('resume-', 'letter-', 1)
    letter_path = abs_path.parent / letter_name
    if letter_path.is_file():
        try:
            with open(letter_path) as f:
                letter = json.load(f)
            data.update(letter)
        except Exception:
            pass

    _json_response(handler, data)


class ResumeHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        from src.utils.logging_manager import get_logger
        get_logger('resume-machine.server').info(fmt % args)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path in ('/', ''):
            self._serve_html()
        elif path == '/api/years':
            _api_years(self)
        elif path == '/api/jobs':
            _api_jobs(self, params)
        elif path == '/api/resume':
            _api_resume(self)
        elif path == '/api/correlation':
            _api_correlation(self, params)
        else:
            _error(self, 404, f'Not found: {path}')

    def _serve_html(self):
        if not _HTML_FILE.is_file():
            _error(self, 404, 'resume-machine.html not found')
            return
        body = _HTML_FILE.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main(argv: list[str] | None = None) -> int:
    _require_venv()
    parser = argparse.ArgumentParser(description='Resume machine local server')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args(argv)

    from src.utils.logging_manager import get_logger, set_level
    cfg = _get_config()
    set_level(cfg.get('log_level', 'info'))
    logger = get_logger('resume-machine.server')

    server = HTTPServer(('localhost', args.port), ResumeHandler)
    logger.info('Serving on localhost:%d', args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('Server stopped')
    return 0


if __name__ == '__main__':
    sys.exit(main())
