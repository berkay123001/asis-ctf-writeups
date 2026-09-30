#!/usr/bin/env python3
"""Download RPROFILE0001-0006 from dpp.asisctf.com and stitch the ADN flag."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "https://dpp.asisctf.com"
PYSIM = Path("/tmp/pysim")
VENV_PY = Path("/tmp/pysimvenv/bin/python")
CLIENT = PYSIM / "contrib" / "es9p_client.py"
OUT = HERE / "out"
MIDS = [f"RPROFILE{i:04d}" for i in range(1, 7)]
ADN_RE = re.compile(rb"\x80([\x01-\x0f])([ -~]{1,15})\x06\x81\x15U")


def download(mid: str) -> Path:
    cmd = [
        str(VENV_PY),
        str(CLIENT),
        "--url",
        BASE,
        "--server-ca-cert",
        str(HERE / "ci.pem"),
        "--certificate-path",
        str(HERE),
        "--euicc-certificate",
        "euicc.der",
        "--euicc-private-key",
        "euicc.key",
        "--eum-certificate",
        "eum.der",
        "--ci-certificate",
        "ci.der",
        "download",
        "--matchingId",
        mid,
        "--output-path",
        str(OUT),
    ]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(PYSIM) + os.pathsep + env.get("PYTHONPATH", "")
    p = subprocess.run(cmd, cwd=str(HERE), env=env, capture_output=True, text=True)
    blob = p.stdout + p.stderr
    m = re.search(r"Storing files as (.+)\.\*\.der", blob)
    if p.returncode != 0 or not m:
        raise SystemExit(f"{mid} failed:\n{blob[-1500:]}")
    return Path(m.group(1) + ".upp.der")


def adn_alpha(upp: bytes) -> str:
    hits = []
    for m in ADN_RE.finditer(upp):
        s = m.group(2).decode("ascii")
        if s in ("test contact", "John Doe") or s.startswith("tel:"):
            continue
        if any(c.isalpha() for c in s) and len(s) >= 3:
            hits.append(s)
    if not hits:
        raise SystemExit("no ADN alpha in UPP")
    return hits[0]


def main() -> None:
    if not CLIENT.is_file() or not VENV_PY.is_file():
        raise SystemExit("need /tmp/pysim and /tmp/pysimvenv (osmocom/pysim es9p_client)")
    OUT.mkdir(exist_ok=True)
    parts = []
    for mid in MIDS:
        upp_path = download(mid)
        part = adn_alpha(upp_path.read_bytes())
        print(f"{mid} {part}")
        parts.append(part)
    flag = "".join(parts)
    if not flag.startswith("ASIS{") or not flag.endswith("}"):
        raise SystemExit(f"bad stitch {flag!r}")
    (HERE / "FLAG").write_text(flag + "\n")
    print(flag)


if __name__ == "__main__":
    sys.exit(main())
