import copy
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import review  # noqa: E402

DEMO = os.path.join(ROOT, "docs", "demo-factcheck.py")


def _load_demo():
    spec = importlib.util.spec_from_file_location("demo_factcheck", DEMO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_demo_uses_list_form_not_shell():
    mod = _load_demo()
    assert "shell=True" not in mod.DIFF
    assert 'subprocess.run(["mv", filename, path])' in mod.DIFF


def test_demo_check_keeps_two_and_drops_one():
    mod = _load_demo()
    kept, dropped = review.check(mod.DIFF, copy.deepcopy(mod.FINDINGS))
    assert dropped == 1
    assert len(kept) == 2
    assert kept[0]["line"] == 12
    assert "line_unverified" not in kept[0]
    assert kept[1].get("line_unverified") is True
