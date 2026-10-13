"""File integrity checker using SHA-256.

Usage:
  python file_integrity.py init  <folder>   # create baseline.json
  python file_integrity.py check <folder>   # compare against baseline.json
"""
import hashlib
import json
import os
import sys

BASELINE = "baseline.json"


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(folder: str) -> dict:
    result = {}
    for root, _, files in os.walk(folder):
        for name in files:
            p = os.path.join(root, name)
            result[os.path.relpath(p, folder)] = sha256(p)
    return result


def init(folder: str):
    data = scan(folder)
    with open(BASELINE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Baseline saved for {len(data)} files.")


def check(folder: str):
    with open(BASELINE) as f:
        old = json.load(f)
    new = scan(folder)
    modified = [p for p in old if p in new and old[p] != new[p]]
    deleted = [p for p in old if p not in new]
    added = [p for p in new if p not in old]
    for p in modified: print("MODIFIED:", p)
    for p in deleted: print("DELETED: ", p)
    for p in added: print("ADDED:   ", p)
    if not (modified or deleted or added):
        print("OK: no changes detected.")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("init", "check"):
        print(__doc__)
        sys.exit(1)
    (init if sys.argv[1] == "init" else check)(sys.argv[2])
