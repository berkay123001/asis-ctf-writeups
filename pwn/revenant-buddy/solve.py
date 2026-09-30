#!/usr/bin/env python3
"""Revenant Buddy — capability-typed VM export.

Worker speaks RB/2. RUN takes hex-encoded 32-bit words. After a fixed
obfuscation layer, the program is a tiny 8-register machine:

  r7 starts as the /dev/urandom session secret (type 2)
  r0 starts as 0 (type 0); r1..r6 start as type 1

  0x8d dest, src1     dest = mixhash(src1)     requires type(src1)==2, dest type 4
  0xd9 dest, src1, src2, imm
                      dest = ((imm+1)&0x7fff)*src2 ^ src1
                      requires type(src1) in {2,4}, type(src2)==0, imm!=0
                      dest type 1  (imm=0x7fff copies src1)
  0x9e dest, src1     if dest==secret and src1==mixhash(secret): print flag
                      requires both types == 1
  0xdc                halt (must be last; verifier requires a prior 0x9e)

Program: hash r7 into r1, copy both values down to type-1 regs, export.
"""
from __future__ import annotations

import struct
from pathlib import Path

from pwn import ELF, context, remote

context.log_level = "info"

HERE = Path(__file__).resolve().parent
WORKER = HERE / "Revenant-Buddy" / "revenant-worker"
HOST, PORT = "91.107.151.102", 18113

MAGIC = 0xEFC6AB35
OP_8D, OP_D9, OP_9E, OP_DC = 0x8D, 0xD9, 0x9E, 0xDC


def rol32(x: int, n: int) -> int:
    n &= 31
    x &= 0xFFFFFFFF
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def ror32(x: int, n: int) -> int:
    n &= 31
    x &= 0xFFFFFFFF
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF


def load_tables(path: Path) -> tuple[bytes, list[int]]:
    elf = ELF(str(path), checksec=False)
    sbox = elf.read(0x93A60, 256)
    tab = [
        struct.unpack_from("<I", elf.read(0x93B60, 256), i)[0]
        for i in range(0, 256, 4)
    ]
    return sbox, tab


def encrypt_words(plains: list[int], sbox: bytes, tab: list[int]) -> list[int]:
    r11, ebx, ebp = 0x11, 0x3, 0x5B
    out = []
    for i, p in enumerate(plains):
        ks = (sbox[r11 & 0xFF] << 24) | (sbox[ebx & 0xFF] << 11) | sbox[ebp & 0xFF]
        x = p ^ 0x7824F328
        x = ror32(x, (i % 29) + 1)
        x ^= tab[i]
        x ^= ks & 0xFFFFFFFF
        out.append(x & 0xFFFFFFFF)
        r11 = (r11 + 0x1D) & 0xFFFFFFFF
        ebx = (ebx + 0x2F) & 0xFFFFFFFF
        ebp = (ebp + 0x0B) & 0xFFFFFFFF
    return out


def insn(op: int, dest: int = 0, src1: int = 0, src2: int = 0, imm: int = 0) -> int:
    return (
        (op & 0xFF)
        | ((dest & 7) << 8)
        | ((src1 & 7) << 11)
        | ((src2 & 7) << 14)
        | ((imm & 0x7FFF) << 17)
    )


def build_program(sbox: bytes, tab: list[int]) -> str:
    prog = [
        MAGIC,
        insn(OP_8D, dest=1, src1=7),  # r1 = hash(secret), type 4
        insn(OP_D9, dest=2, src1=7, src2=0, imm=0x7FFF),  # r2 = secret, type 1
        insn(OP_D9, dest=3, src1=1, src2=0, imm=0x7FFF),  # r3 = hash, type 1
        insn(OP_9E, dest=2, src1=3),  # export flag
        insn(OP_DC),  # halt (verifier)
    ]
    enc = encrypt_words(prog, sbox, tab)
    return b"".join(struct.pack("<I", w) for w in enc).hex()


def main() -> None:
    sbox, tab = load_tables(WORKER)
    payload = build_program(sbox, tab)
    r = remote(HOST, PORT)
    banner = r.recvline()
    print(banner.decode().strip())
    r.sendline(b"RUN " + payload.encode())
    print(r.recvline().decode().strip())
    r.close()


if __name__ == "__main__":
    main()
