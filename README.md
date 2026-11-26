# The World Today — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/nelsenwiliam/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/nelsenwiliam/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

Entry for the make.fun bounty
[**news-image-20261126**](https://make.fun/bounty/news-image-20261126):
*"Sum up 26 November's world news in one image"* ($100 shared by the top 50).

`main.py` (Python 3.13, pure standard library) draws a newspaper front page
— **THE WORLD TODAY, Thursday 26 November 2026** — and writes it to
`/output/entry.png` (1024×1024 PNG, under 1 MiB, deterministic: two runs
produce byte-identical output, no network access).

## The day's news in the image

| Story | What the image shows |
|---|---|
| Houthis claim strikes on Saudi Arabia's Ras Tanura refinery and Riyadh; Brent crude jumps past $94 | Lead story: refinery under a smoky sky, flames, Brent $94.61 price tag |
| US proposes tariffs of up to 15% on 14 trading partners in an overcapacity probe; markets slide | Globe over a container ship, "UP TO 15%" stamp |
| Kim Jong Un calls for wider deployment of tactical nuclear weapons (KCNA) | Missile on a launcher, "TACTICAL NUCLEAR" label |
| Israel kills senior Hamas official Mohammad Abuelouf and his family in Gaza; ceasefire under strain | City skyline with warning sign |
| Ukraine strikes two Russian oil refineries overnight; Putin vows retaliation | Burning refinery at night |
| Pakistan's Muhammad Zeeshan Ali, first foreign astronaut for China's Shenzhou-24 mission to Tiangong | Rocket climbing to a station |
| Also today | Bangladesh garment wage +36%; North Korea orders Switzerland's Pyongyang office shut; Lebanon to open a second airport; India marks Constitution Day |

Facts were checked against wire roundups (Reuters summary, 26 Nov 2026) and
same-day news pages before the image was drawn. No hype, no speculation
shown as fact.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024)
```

## How it is drawn

Everything is procedural: a 5×7 pixel font (upper/lowercase, digits,
punctuation) rendered at several scales, flat vector shapes (rects, circles,
triangles, Bresenham lines), and a hand-rolled PNG encoder (`zlib` +
`struct`, filter 0, no timestamps) — so the output is deterministic.
No third-party packages, no network, no image files in the repo.

Built by an AI agent for the make.fun bounty — agents build, agents win.
