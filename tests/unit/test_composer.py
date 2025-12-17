import os
import sys
import json

HERE = os.path.dirname(os.path.dirname(__file__))
LIB = os.path.join(HERE, "..", "scripts", "_lib")
LIB = os.path.normpath(LIB)
sys.path.insert(0, LIB)

from composer import Composer


def test_merge_simple_override():
    base = {"name": "Jane", "skills": ["python"]}
    frag = {"name": "Janet", "skills": ["go"]}
    c = Composer()
    merged = c.merge(base, [frag])
    assert merged["name"] == "Janet"
    assert merged["skills"] == ["python", "go"]


def test_merge_nested_dict():
    base = {"work": {"company": "A", "details": {"years": 2}}}
    frag = {"work": {"details": {"years": 3, "role": "senior"}}}
    c = Composer()
    merged = c.merge(base, [frag])
    assert merged["work"]["company"] == "A"
    assert merged["work"]["details"]["years"] == 3
    assert merged["work"]["details"]["role"] == "senior"
