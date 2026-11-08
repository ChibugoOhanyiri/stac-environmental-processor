"""Inspect a small GeoTIFF exported from Earth Engine, using only the Python standard library.

Prints size, bands, pixel size, CRS (EPSG), origin, band names and per-band statistics.
Written for M1 (2026-09-28) because Pillow cannot open multi-band float GeoTIFFs and no
raster library is installed yet (M2 will add a pinned rasterio/GDAL stack).

Limits: BigTIFF or classic TIFF; a single tile or strip; LZW (5), Deflate (8) or no compression;
float32 pixels; horizontal predictor 1 only. Anything else raises a clear error.
Usage: .venv/bin/python scripts/inspect_geotiff.py outputs/sample.tif
"""
from __future__ import annotations

import math
import struct
import sys
import zlib
from pathlib import Path

TYPES = {1: ("B", 1), 2: ("s", 1), 3: ("H", 2), 4: ("I", 4), 11: ("f", 4), 12: ("d", 8), 16: ("Q", 8)}


def lzw_decode(data: bytes) -> bytes:
    """TIFF-flavoured LZW: MSB-first codes, 9–12 bits, 'early change'."""
    out, table = bytearray(), [bytes([i]) for i in range(256)] + [b"", b""]
    bitpos, nbits, prev, total = 0, 9, None, len(data) * 8
    while True:
        if bitpos + nbits > total:
            break
        code = 0
        for _ in range(nbits):
            code = (code << 1) | ((data[bitpos >> 3] >> (7 - (bitpos & 7))) & 1)
            bitpos += 1
        if code == 257:
            break
        if code == 256:
            table, nbits, prev = table[:258], 9, None
            continue
        if prev is None:
            entry = table[code]
        elif code < len(table):
            entry = table[code]
            table.append(prev + entry[:1])
        else:
            entry = prev + prev[:1]
            table.append(entry)
        out += entry
        prev = entry
        if prev is not None and len(table) + 1 >= (1 << nbits) and nbits < 12:
            nbits += 1
    return bytes(out)


def read_tags(d: bytes):
    bo = {b"II": "<", b"MM": ">"}[d[:2]]
    big = struct.unpack(bo + "H", d[2:4])[0] == 43
    if big:
        off, cfmt, esize, vsize = struct.unpack(bo + "Q", d[8:16])[0], "Q", 20, 8
    else:
        off, cfmt, esize, vsize = struct.unpack(bo + "I", d[4:8])[0], "H", 12, 4
    csize = 8 if big else 2
    n = struct.unpack(bo + cfmt, d[off:off + csize])[0]
    tags = {}
    for i in range(n):
        e = d[off + csize + esize * i: off + csize + esize * (i + 1)]
        tag, typ = struct.unpack(bo + "HH", e[:4])
        cnt = struct.unpack(bo + ("Q" if big else "I"), e[4:4 + (8 if big else 4)])[0]
        if typ not in TYPES:
            continue
        fmt, size = TYPES[typ]
        vfield = e[esize - vsize:]
        raw = vfield if size * cnt <= vsize else d[struct.unpack(bo + ("Q" if big else "I"), vfield)[0]:][:size * cnt]
        tags[tag] = raw[:cnt].rstrip(b"\0").decode("latin1") if typ == 2 else struct.unpack(bo + fmt * cnt, raw[:size * cnt])
    return bo, tags


def main(path: str) -> int:
    d = Path(path).read_bytes()
    bo, t = read_tags(d)
    width, height, bands = t[256][0], t[257][0], t.get(277, (1,))[0]
    comp, pred = t.get(259, (1,))[0], t.get(317, (1,))[0]
    geokeys = t.get(34735, ())
    # GeoKey directory: a 4-number header, then (key, location, count, value) entries.
    # Key 3072 = projected CRS, 2048 = geographic CRS.
    epsg = next((geokeys[4 * i + 3] for i in range(1, len(geokeys) // 4) if geokeys[4 * i] in (3072, 2048)), None)
    print(f"size: {width} x {height} pixels, {bands} band(s), compression={comp}, predictor={pred}")
    if 33550 in t:
        print(f"pixel size: {t[33550][0]} x {t[33550][1]} (CRS units)")
    if 33922 in t:
        print(f"top-left corner: x={t[33922][3]}, y={t[33922][4]}")
    print(f"CRS: EPSG:{epsg}")
    names = []
    if 42112 in t:
        names = [line.split(">")[1].split("<")[0] for line in t[42112].splitlines() if "DESCRIPTION" in line]
        print("band names:", names)
    offsets, counts = t.get(324) or t.get(273), t.get(325) or t.get(279)
    if len(offsets) != 1 or t.get(339, (3,))[0] != 3 or pred != 1 or comp not in (1, 5, 8):
        raise SystemExit("Unsupported layout for this simple reader; use rasterio in M2.")
    raw = d[offsets[0]:offsets[0] + counts[0]]
    raw = {1: lambda b: b, 5: lzw_decode, 8: zlib.decompress}[comp](raw)
    tile_w = t.get(322, (width,))[0]
    vals = struct.unpack(bo + "f" * (len(raw) // 4), raw)
    for b in range(bands):
        v = [vals[(y * tile_w + x) * bands + b] for y in range(height) for x in range(width)]
        good = sorted(x for x in v if not math.isnan(x))
        mean_db = 10 * math.log10(sum(10 ** (x / 10) for x in good) / len(good))
        label = names[b] if b < len(names) else f"band {b + 1}"
        print(f"{label}: valid={len(good)} nodata={len(v) - len(good)} min={good[0]:.2f} "
              f"median={good[len(good) // 2]:.2f} max={good[-1]:.2f} mean(linear->dB)={mean_db:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "outputs/sample.tif"))
