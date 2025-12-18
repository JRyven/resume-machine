import os
import sys
import json
import tempfile

HERE = os.path.dirname(os.path.dirname(__file__))
LIB = os.path.join(HERE, "..", "scripts")
LIB = os.path.normpath(LIB)
sys.path.insert(0, LIB)

from build_resume import main as build_main


def write_yaml(path: str, data: dict):
    import yaml

    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f)


def test_dry_run_writes_json(tmp_path, monkeypatch):
    base = {"basics": {"name": "James Valeii"}, "skills": ["python"]}
    frag = {"skills": ["go"]}

    base_path = tmp_path / "base.yaml"
    frag_path = tmp_path / "frag.yaml"
    write_yaml(str(base_path), base)
    write_yaml(str(frag_path), frag)

    outdir = tmp_path / "out"
    args = ["--base", str(base_path), "--fragments", str(frag_path), "--output-dir", str(outdir), "--dry-run"]
    rc = build_main(args)
    assert rc == 0
    # JSON should exist
    jpath = outdir / "resume.json"
    assert jpath.exists()
    data = json.loads(jpath.read_text(encoding="utf-8"))
    assert data["basics"]["name"] == "James Valeii"
    assert "go" in data["skills"]


def test_calls_resumed(monkeypatch, tmp_path):
    base = {"basics": {"name": "Alice Example"}}
    base_path = tmp_path / "base.yaml"
    import yaml

    with open(base_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(base, f)

    outdir = tmp_path / "out"
    called = {}

    def fake_run(cmd, check):
        called["cmd"] = cmd
        return 0

    monkeypatch.setattr("subprocess.run", fake_run)
    args = ["--base", str(base_path), "--output-dir", str(outdir)]
    rc = build_main(args)
    assert rc == 0
    assert "resumed" in called["cmd"][0]
