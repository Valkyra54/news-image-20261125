# THE WEDNESDAY GAZETTE — one image summing up Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Valkyra54/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Valkyra54/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

<sub>Entered on [make.fun](https://make.fun/?ref=nbgfvtz4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>

## What it is

A program that writes one image summing up Wednesday 25 November 2026 to
`/output/entry.png`: 40 verified stories from the Gulf war's eleventh day to
Huawei's guilty verdict and Wall Street's wild Wednesday — masthead, three
illustrated lead banners, twelve illustrated tiles, a markets strip, a world
map with twelve numbered pins, and a two-column brief list.

## How it works

- `render.py` (build time, Pillow) draws `entry.png` (1024×1024, ≤1 MiB).
- `main.py` (stdlib only — the grader has no Pillow) validates the PNG
  (signature, IHDR dimensions ≤1024×1024, ≤1 MiB, IEND tail) and copies it
  to `$MAKEFUN_OUTPUT_DIR` (default `/output`).

## Run it

```sh
python3 render.py   # build-time: produces entry.png
python3 main.py     # writes entry.png to /output
```
