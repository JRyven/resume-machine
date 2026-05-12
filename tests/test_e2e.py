"""
End-to-end integration test for resume-machine.

Starts a real HTTPServer on an ephemeral port and exercises every API
endpoint, including path-traversal guard, using only stdlib.

Run with:
  python -m pytest tests/ -v
  python -m unittest tests.test_e2e
"""

import http.client
import json
import sys
import threading
import unittest
from http.server import HTTPServer
from pathlib import Path

# ── Ensure project root is importable (covers running as plain unittest) ──
_PROJECT_ROOT = Path(__file__).parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.api.serve import ResumeHandler  # noqa: E402 – must follow sys.path setup


# ── Helpers ───────────────────────────────────────────────────────────────

def _get(port: int, path: str) -> tuple[int, object]:
    conn = http.client.HTTPConnection('localhost', port, timeout=5)
    conn.request('GET', path)
    resp = conn.getresponse()
    body = resp.read()
    conn.close()
    try:
        return resp.status, json.loads(body)
    except Exception:
        return resp.status, body


def _get_raw(port: int, path: str) -> tuple[int, bytes, str]:
    """Return (status, body_bytes, content_type)."""
    conn = http.client.HTTPConnection('localhost', port, timeout=5)
    conn.request('GET', path)
    resp = conn.getresponse()
    body = resp.read()
    ct = resp.getheader('Content-Type', '')
    conn.close()
    return resp.status, body, ct


# ── Test case ─────────────────────────────────────────────────────────────

class TestE2E(unittest.TestCase):
    """Full stack tests against a live server instance."""

    @classmethod
    def setUpClass(cls):
        # Port 0 lets the OS assign a free port
        cls.server = HTTPServer(('localhost', 0), ResumeHandler)
        cls.port = cls.server.server_address[1]
        cls._thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls._thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    # ── GET / ─────────────────────────────────────────────────────────────

    def test_root_returns_html(self):
        status, body, ct = _get_raw(self.port, '/')
        self.assertEqual(status, 200)
        self.assertIn('text/html', ct)
        self.assertIn(b'<!DOCTYPE html>', body)
        self.assertIn(b'Resume Machine', body)

    def test_unknown_route_returns_404(self):
        status, data = _get(self.port, '/api/doesnotexist')
        self.assertEqual(status, 404)
        self.assertIn('error', data)

    # ── GET /api/years ────────────────────────────────────────────────────

    def test_years_returns_200_list(self):
        status, data = _get(self.port, '/api/years')
        self.assertEqual(status, 200)
        self.assertIsInstance(data, list)

    def test_years_contains_2026(self):
        _, data = _get(self.port, '/api/years')
        self.assertIn('2026', data)

    def test_years_sorted_descending(self):
        _, data = _get(self.port, '/api/years')
        self.assertEqual(data, sorted(data, reverse=True))

    # ── GET /api/jobs ─────────────────────────────────────────────────────

    def test_jobs_returns_list_for_2026(self):
        status, data = _get(self.port, '/api/jobs?year=2026')
        self.assertEqual(status, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_jobs_entry_has_required_fields(self):
        _, data = _get(self.port, '/api/jobs?year=2026')
        first = data[0]
        for field in ('path', 'job_title', 'employer', 'domain'):
            self.assertIn(field, first, f'Missing field: {field}')

    def test_jobs_month_filter_returns_subset(self):
        _, all_jobs = _get(self.port, '/api/jobs?year=2026')
        _, month_jobs = _get(self.port, '/api/jobs?year=2026&month=4')
        self.assertIsInstance(month_jobs, list)
        # Month-filtered result must be a subset of year result
        all_paths = {j['path'] for j in all_jobs}
        for j in month_jobs:
            self.assertIn(j['path'], all_paths)

    def test_jobs_missing_year_returns_400(self):
        status, data = _get(self.port, '/api/jobs')
        self.assertEqual(status, 400)
        self.assertIn('error', data)

    def test_jobs_nonexistent_year_returns_empty(self):
        status, data = _get(self.port, '/api/jobs?year=1900')
        self.assertEqual(status, 200)
        self.assertEqual(data, [])

    # ── GET /api/resume ───────────────────────────────────────────────────

    def test_resume_returns_200(self):
        status, data = _get(self.port, '/api/resume')
        self.assertEqual(status, 200)
        self.assertIn('basics', data)
        self.assertIn('work', data)

    def test_resume_basics_has_name(self):
        _, data = _get(self.port, '/api/resume')
        self.assertIn('name', data['basics'])
        self.assertTrue(data['basics']['name'])

    def test_resume_has_no_placeholders(self):
        _, data = _get(self.port, '/api/resume')
        raw = json.dumps(data)
        self.assertNotIn('{{', raw, 'Unresolved placeholder found in resume data')

    # ── GET /api/correlation ──────────────────────────────────────────────

    def _first_named_job(self) -> str | None:
        """Return path of first correlation file with a known employer."""
        _, jobs = _get(self.port, '/api/jobs?year=2026')
        named = [j for j in jobs if j.get('employer', 'unknown') not in ('', 'unknown')]
        return named[0]['path'] if named else None

    def test_correlation_valid_path_returns_200(self):
        path = self._first_named_job()
        if path is None:
            self.skipTest('No named-employer correlation files found')
        status, data = _get(self.port, f'/api/correlation?path={path}')
        self.assertEqual(status, 200)

    def test_correlation_has_required_keys(self):
        path = self._first_named_job()
        if path is None:
            self.skipTest('No named-employer correlation files found')
        _, data = _get(self.port, f'/api/correlation?path={path}')
        for key in ('correlations', 'metadata', 'domain'):
            self.assertIn(key, data, f'Missing key: {key}')

    def test_correlation_merges_cover_letter(self):
        path = self._first_named_job()
        if path is None:
            self.skipTest('No named-employer correlation files found')
        _, data = _get(self.port, f'/api/correlation?path={path}')
        self.assertIn('opening', data, 'Cover letter not merged into correlation response')

    def test_correlation_missing_path_param_returns_400(self):
        status, data = _get(self.port, '/api/correlation')
        self.assertEqual(status, 400)
        self.assertIn('error', data)

    # ── Path-traversal guard ──────────────────────────────────────────────

    def test_traversal_simple_dotdot_blocked(self):
        status, data = _get(self.port, '/api/correlation?path=../../etc/passwd')
        self.assertEqual(status, 400)
        self.assertIn('error', data)

    def test_traversal_encoded_dotdot_blocked(self):
        status, data = _get(self.port, '/api/correlation?path=..%2F..%2Fetc%2Fpasswd')
        self.assertEqual(status, 400)
        self.assertIn('error', data)

    def test_traversal_nested_dotdot_blocked(self):
        status, data = _get(
            self.port,
            '/api/correlation?path=data/job-listings/../../../etc/passwd',
        )
        self.assertEqual(status, 400)
        self.assertIn('error', data)

    def test_traversal_absolute_path_blocked(self):
        status, data = _get(self.port, '/api/correlation?path=/etc/passwd')
        self.assertEqual(status, 400)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()
