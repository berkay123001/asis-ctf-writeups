"""Atarude (ASIS CTF) - binary'den cikarilan ilkellerin Python karsiligi."""
from pathlib import Path

BIN = Path(__file__).resolve().parent.parent / "Atarude" / "Atarude"
DATA = BIN.read_bytes()
TABLE_OFF = 0x5064
MOD = 0xC0FFE0

def table_digest() -> bytes:
    """0x1800 turluk xorshift64 tabanli sabit ozet (rodata tablosunun 16 baytlik ozeti)."""
    st = bytearray(16)
    x = 0x9E3779B97F4A7C15
    d = 0
    M = (1 << 64) - 1
    for i in range(0x1800):
        x = (x ^ (x << 13)) & M
        x ^= x >> 7
        x = (x ^ (x << 17)) & M
        j = i & 0xF
        r = i & 7
        s = (x ^ d) % MOD
        t = st[j]
        t = ((t << r) | (t >> (8 - r))) & 0xFF
        t ^= DATA[TABLE_OFF + s]
        t ^= DATA[TABLE_OFF + s + 0x11]
        t ^= (x >> 0x29) & 0xFF
        st[j] = t
        d += 0x9E37
    return bytes(st)

# ---- AES-128 (binary yazilim implementasyonuyla ayni) ----
_SBOX = None
def _mk_sbox():
    global _SBOX
    p = q = 1
    sbox = [0] * 256
    while True:
        p = p ^ ((p << 1) & 0xFF) ^ (0x1B if p & 0x80 else 0)
        q ^= q << 1; q ^= q << 2; q ^= q << 4; q &= 0xFF
        if q & 0x80: q ^= 0x09
        x = q ^ ((q << 1) | (q >> 7)) ^ ((q << 2) | (q >> 6)) ^ ((q << 3) | (q >> 5)) ^ ((q << 4) | (q >> 4))
        sbox[p] = (x ^ 0x63) & 0xFF
        if p == 1: break
    sbox[0] = 0x63
    _SBOX = sbox
_mk_sbox()

def _xtime(a): return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else a << 1

def _expand(key):
    w = [list(key[i*4:i*4+4]) for i in range(4)]
    rcon = 1
    for i in range(4, 44):
        t = list(w[i-1])
        if i % 4 == 0:
            t = t[1:] + t[:1]
            t = [_SBOX[b] for b in t]
            t[0] ^= rcon
            rcon = _xtime(rcon)
        w.append([w[i-4][j] ^ t[j] for j in range(4)])
    return [bytes(b for wd in w[4*r:4*r+4] for b in wd) for r in range(11)]

def aes_encrypt(key: bytes, block: bytes) -> bytes:
    rk = _expand(key)
    s = bytes(a ^ b for a, b in zip(block, rk[0]))
    for r in range(1, 11):
        s = bytes(_SBOX[b] for b in s)
        s = bytes(s[(i + 4 * (i % 4)) % 16] for i in range(16))  # ShiftRows
        if r != 10:
            out = bytearray(16)
            for c in range(4):
                col = s[4*c:4*c+4]
                for i in range(4):
                    out[4*c+i] = (_xtime(col[i]) ^ (_xtime(col[(i+1) % 4]) ^ col[(i+1) % 4])
                                  ^ col[(i+2) % 4] ^ col[(i+3) % 4])
            s = bytes(out)
        s = bytes(a ^ b for a, b in zip(s, rk[r]))
    return s

K = table_digest()

def mac(dom: int, msg: bytes) -> bytes:
    """S = K; her 16 baytlik blok icin S = AES_K(tweak_i ^ m_i ^ S); sonuc AES_S(K)."""
    assert len(msg) % 16 == 0
    S = K
    for i in range(len(msg) // 16):
        tw = bytes((dom + 11 * j + 29 * i) & 0xFF for j in range(16))
        blk = bytes(tw[j] ^ msg[16*i+j] ^ S[j] for j in range(16))
        S = aes_encrypt(K, blk)
    return aes_encrypt(S, K)

if __name__ == "__main__":
    print("K =", K.hex())
