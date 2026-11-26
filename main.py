#!/usr/bin/env python3
"""Entry point for THE WEDNESDAY GAZETTE (news-image-20261125).

Stdlib only: validates the pre-rendered entry.png and copies it to the
output directory. Never deletes the output directory itself.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024
MAX_DIM = 1024


def fail(msg):
    sys.stderr.write("error: %s\n" % msg)
    return 1


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not os.path.isfile(SRC):
        return fail("entry.png not found next to main.py")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        return fail("entry.png exceeds 1 MiB (%d bytes)" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("entry.png is not a PNG (bad signature)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        return fail("entry.png dims %dx%d exceed 1024x1024" % (width, height))
    if data[-12:-8] != b"IEND" and data[-8:-4] != b"IEND":
        return fail("entry.png has no IEND tail")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    sys.stdout.write("ok: wrote %s (%d bytes, %dx%d)\n"
                     % (dst, len(data), width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
