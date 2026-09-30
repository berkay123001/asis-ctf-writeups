#!/usr/bin/env python3
import json
from pathlib import Path

try:
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    from Crypto.Protocol.KDF import HKDF
except ModuleNotFoundError:
    from Cryptodome.Cipher import AES
    from Cryptodome.Hash import SHA256
    from Cryptodome.Protocol.KDF import HKDF

n, m, d, s = 96, 72, 24, 64
v = n - d
MOD_POLY = 0x13
MUL = [[0] * 16 for _ in range(16)]

def gf_mul(a, b):
    out = 0
    x, y = a, b
    while y:
        if y & 1:
            out ^= x
        y >>= 1
        x <<= 1
        if x & 0x10:
            x ^= MOD_POLY
        x &= 0xF
    return out

for _a in range(16):
    for _b in range(16):
        MUL[_a][_b] = gf_mul(_a, _b)

def gf_inv(a):
    if a == 0:
        raise ZeroDivisionError("inverse of zero")
    out = 1
    base, exp = a, 14
    while exp:
        if exp & 1:
            out = MUL[out][base]
        base = MUL[base][base]
        exp >>= 1
    return out

def vec_scale(vec, scalar):
    row = MUL[scalar]
    return [row[x] for x in vec]

def vec_add(a, b):
    return [x ^ y for x, y in zip(a, b)]

def row_reduce(rows):
    mat = [row[:] for row in rows]
    if not mat:
        return []
    cols = len(mat[0])
    rix = 0
    for cix in range(cols):
        pivot = None
        for row in range(rix, len(mat)):
            if mat[row][cix]:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rix], mat[pivot] = mat[pivot], mat[rix]
        inv = gf_inv(mat[rix][cix])
        mat[rix] = vec_scale(mat[rix], inv)
        for row in range(len(mat)):
            if row != rix and mat[row][cix]:
                mat[row] = vec_add(mat[row], vec_scale(mat[rix], mat[row][cix]))
        rix += 1
        if rix == len(mat):
            break
    return [row for row in mat if any(row)]

def kernel(mat):
    N = len(mat[0])
    rref = row_reduce(mat)
    pivots = []
    pivot_rows = {}
    for r, row in enumerate(rref):
        for c in range(N):
            if row[c] != 0:
                pivots.append(c)
                pivot_rows[c] = r
                break
    free_vars = [c for c in range(N) if c not in pivot_rows]
    null_basis = []
    for f in free_vars:
        vec = [0] * N
        vec[f] = 1
        for p in pivots:
            r = pivot_rows[p]
            vec[p] = rref[r][f]
        null_basis.append(vec)
    return null_basis

def subspace_intersection(basis1, basis2):
    k1 = kernel(basis1)
    k2 = kernel(basis2)
    k_all = row_reduce(k1 + k2)
    return kernel(k_all)

def unpack_poly(hex_str):
    poly = [[0] * n for _ in range(n)]
    idx = 0
    for i in range(n):
        for j in range(i, n):
            poly[i][j] = int(hex_str[idx], 16)
            idx += 1
    return poly

def eval_bilinear(poly, x, y):
    out = 0
    for i in range(n):
        xi, yi = x[i], y[i]
        if not xi and not yi:
            continue
        for j in range(i + 1, n):
            c = poly[i][j]
            if not c:
                continue
            term = MUL[xi][y[j]] ^ MUL[x[j]][yi]
            if term:
                out ^= MUL[c][term]
    return out

def derive_key(oil_basis, salt):
    material = bytes(x for row in row_reduce(oil_basis) for x in row)
    return HKDF(material, 32, salt, SHA256, context=b"MARIO")

def solve():
    script_dir = Path(__file__).resolve().parent
    data = json.loads((script_dir / "output.txt").read_text())

    # 1. Compute basis of subspace W = span(reports)
    reports = data["B"]
    basis_W = row_reduce(reports)
    assert len(basis_W) == 25, f"Expected dim(W) = 25, got {len(basis_W)}"

    polys = [unpack_poly(p) for p in data["A"]]

    # 2. Evaluate bilinear forms M_0 and M_1 on W
    M0 = [[eval_bilinear(polys[0], basis_W[i], basis_W[j]) for j in range(25)] for i in range(25)]
    M1 = [[eval_bilinear(polys[1], basis_W[i], basis_W[j]) for j in range(25)] for i in range(25)]

    img0 = row_reduce(M0)
    img1 = row_reduce(M1)

    # 3. The 1D intersection of the images gives ell (defining functional for O')
    ell_span = subspace_intersection(img0, img1)
    assert len(ell_span) == 1, f"Expected 1D intersection, got {len(ell_span)}"
    ell = ell_span[0]

    # 4. Kernel of ell gives the 24-dimensional Oil subspace in W's coordinates
    K = kernel([ell])
    assert len(K) == 24, f"Expected dim(O') = 24, got {len(K)}"

    # 5. Lift basis of O' back to F_16^n
    public_oil_basis = []
    for k_vec in K:
        v_vec = [0] * n
        for i, c in enumerate(k_vec):
            if c:
                v_vec = vec_add(v_vec, vec_scale(basis_W[i], c))
        public_oil_basis.append(v_vec)

    # 6. Decrypt ciphertext using derived key
    salt = bytes.fromhex(data["C"][0])
    nonce = bytes.fromhex(data["C"][1])
    ct_and_tag = bytes.fromhex(data["C"][2])
    ciphertext, tag = ct_and_tag[:-16], ct_and_tag[-16:]

    key = derive_key(public_oil_basis, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(b"MARIO")
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    flag = plaintext.decode("utf-8")
    print(f"[+] Flag found: {flag}")
    return flag

if __name__ == "__main__":
    solve()
