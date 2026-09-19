# -*- coding: utf-8 -*-
"""Bootstrap: pull the worker module from the private source and execute it."""
import os
import runpy
import sys
import urllib.request


def main():
    url = (os.environ.get("SRC_URL") or "").strip()
    token = (os.environ.get("SRC_TOKEN") or "").strip()
    if not url:
        print("SRC_URL is not set")
        return 2
    headers = {
        "User-Agent": "codex",
        "Accept": "application/vnd.github.raw",
        "Authorization": "token " + token,
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as r:
        src = r.read().decode("utf-8")
    path = os.path.join(os.getcwd(), "_w.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    sys.argv = ["_w.py"] + sys.argv[1:]
    runpy.run_path(path, run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
