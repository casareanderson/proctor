#!/usr/bin/env python3
"""Produce the fact-check screenshot for the README. No network, no API key.

Runs the real review.check() from review.py with a canned model-style reply over a
sample diff, and prints what survives. The model reply is a fixture; the
fact-checking is the real code path.
"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import review  # noqa: E402

DIFF = """\
diff --git a/app/upload.py b/app/upload.py
index 1111111..2222222 100644
--- a/app/upload.py
+++ b/app/upload.py
@@ -10,7 +10,9 @@ def handle(filename):
     if not filename:
         return
+    path = "/tmp/" + filename
+    subprocess.run("mv " + filename + " " + path, shell=True)
     print("done")
"""

# Canned model-style reply: one real finding, one with a line outside the hunks,
# one naming a file that is not in the diff at all.
FINDINGS = [
    {
        "severity": "high",
        "file": "app/upload.py",
        "line": 12,
        "title": "shell injection",
        "why": "filename from the caller is built straight into a shell command",
    },
    {
        "severity": "med",
        "file": "app/upload.py",
        "line": 50,
        "title": "line outside the patch hunks",
        "why": "line 50 is not part of this diff",
    },
    {
        "severity": "med",
        "file": "app/admin.py",
        "line": 1,
        "title": "hallucinated file",
        "why": "app/admin.py does not appear in this diff",
    },
]


def main():
    print("proctor - fact-check demo (review.check, the real code path; the")
    print("model reply below is canned)")
    print()
    print("Diff under review (adds a shell call built from an untrusted filename):")
    for line in DIFF.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            print("  " + line)
    print()
    original = copy.deepcopy(FINDINGS)
    kept, dropped = review.check(DIFF, FINDINGS)
    print("Model-style reply, then what check() did with each finding:")
    for f in original:
        loc = f"{f['file']}:{f['line']}"
        print(f"  {loc:34s} {f['title']}")
    print()
    print("After check():")
    for f in kept:
        loc = f"{f['file']}:{f['line']}"
        tag = "line cleared (line_unverified)" if f.get("line_unverified") else "line verified"
        print(f"  kept    {loc:34s} {f['title']} - {tag}")
    print(f"  dropped {dropped} finding(s) - file not in the diff")
    print()
    print(f"result: {len(kept)} kept, {dropped} dropped")


if __name__ == "__main__":
    main()
