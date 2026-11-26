#!/usr/bin/env python3
"""News-image entry for make.fun: "Sum up 26 November's world news in one image".

Draws a newspaper front page for Thursday 26 November 2026, pure stdlib only.
Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png), 1024x1024 PNG,
deterministic: two runs produce byte-identical output, no network access.

Stories (all reported on 26 Nov 2026, events of 25-26 Nov 2026):
 1. Houthis claim strikes on Saudi Arabia's Ras Tanura refinery and Riyadh;
    Brent crude jumps past $94 a barrel (Reuters / wire roundups).
 2. US proposes new tariffs of up to 15% on 14 trading partners in a
    Section 301 overcapacity probe; markets fall (USTR, 25 Nov).
 3. Kim Jong Un calls for wider deployment of tactical nuclear weapons
    (KCNA, reported Thursday 26 Nov).
 4. Israel kills senior Hamas official Mohammad Abuelouf and his family in
    Gaza; ceasefire under strain.
 5. Ukraine strikes two Russian oil refineries overnight; Putin vows
    retaliation.
 6. Pakistan's Muhammad Zeeshan Ali becomes the first foreign astronaut
    selected for China's Shenzhou-24 mission to Tiangong.
Briefs: Bangladesh garment wage +36%; North Korea orders Switzerland to
close its Pyongyang office; Lebanon to open a second airport; India marks
Constitution Day and 18 years since the 26/11 Mumbai attacks.
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette ---
PAPER = (247, 242, 231)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
NAVY_LT = (38, 58, 96)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
GOLD_LT = (232, 196, 90)
TEAL = (14, 124, 123)
GREY = (107, 114, 128)
SKY = (196, 216, 228)
SKY_DK = (148, 178, 198)
ORANGE = (234, 88, 12)
FLAME = (245, 158, 11)
WHITE = (255, 255, 255)
GREEN = (22, 101, 52)

# ------------------------------------------------------------- 5x7 font -----
# Each glyph: 7 rows of 5 bits, '1' = ink.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "00010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    'q': ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '*': ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    '#': ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    '>': ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    '<': ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '[': ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    ']': ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
}

CHAR_W = 6  # glyph advance in font units (5 + 1 spacing)


# ---------------------------------------------------------------- canvas ----
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def fill(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            row = yy * self.w * 3
            for xx in range(x0, x1):
                i = row + xx * 3
                self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c, t=1):
        self.fill(x, y, w, t, c)
        self.fill(x, y + h - t, w, t, c)
        self.fill(x, y, t, h, c)
        self.fill(x + w - t, y, t, h, c)

    def hline(self, x, y, w, c, t=1):
        self.fill(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.fill(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d <= r * r:
                        self.set(xx, yy, c)
                else:
                    if abs(d - r * r) <= r:
                        self.set(xx, yy, c)

    def triangle(self, x0, y0, x1, y1, x2, y2, c):
        minx, maxx = min(x0, x1, x2), max(x0, x1, x2)
        miny, maxy = min(y0, y1, y2), max(y0, y1, y2)
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if den == 0:
            return
        for yy in range(miny, maxy + 1):
            for xx in range(minx, maxx + 1):
                a = ((y1 - y2) * (xx - x2) + (x2 - x1) * (yy - y2)) / den
                b = ((y2 - y0) * (xx - x2) + (x0 - x2) * (yy - y2)) / den
                cc = 1 - a - b
                if a >= 0 and b >= 0 and cc >= 0:
                    self.set(xx, yy, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                cx += CHAR_W * scale
                continue
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits[col] == '1':
                        self.fill(cx + col * scale, y + row * scale,
                                  scale, scale, c)
            cx += CHAR_W * scale
        return cx

    def text_w(self, s, scale):
        return sum(CHAR_W for _ in s) * scale - scale

    def wrap(self, s, max_w, scale):
        """Greedy word wrap; returns list of lines fitting max_w pixels."""
        words = s.split(' ')
        lines, cur = [], ''
        for wd in words:
            trial = wd if not cur else cur + ' ' + wd
            if self.text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


# ------------------------------------------------------------------ png -----
def write_png(path, cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        out = struct.pack('>I', len(data)) + tag + data
        out += struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


# -------------------------------------------------------------- artwork -----
def draw_refinery(cv, x, y, w, h):
    """Oil refinery under a smoky sky with flames and a price tag."""
    cv.fill(x, y, w, h, SKY)
    # sun
    cv.circle(x + w - 52, y + 42, 26, GOLD_LT)
    cv.circle(x + w - 52, y + 42, 20, GOLD)
    # smoke puffs
    for sx, sy, r in ((x + 78, y + 34, 16), (x + 104, y + 26, 20),
                      (x + 132, y + 36, 14), (x + 236, y + 30, 18),
                      (x + 262, y + 22, 14)):
        cv.circle(sx, sy, r, (226, 232, 240))
        cv.circle(sx, sy, r - 5, (203, 213, 225))
    # ground
    cv.fill(x, y + h - 46, w, 46, (90, 84, 74))
    # storage tanks
    for tx, tw, th in ((x + 16, 74, 62), (x + 100, 62, 52)):
        cv.fill(tx, y + h - 46 - th, tw, th, (226, 232, 240))
        cv.rect(tx, y + h - 46 - th, tw, th, INK, 2)
        cv.fill(tx, y + h - 46 - th, tw, 8, (148, 163, 184))
    # distillation towers
    for tx, tw, th in ((x + 182, 30, 118), (x + 222, 24, 132)):
        cv.fill(tx, y + h - 46 - th, tw, th, NAVY_LT)
        cv.rect(tx, y + h - 46 - th, tw, th, INK, 2)
        cv.fill(tx - 4, y + h - 46 - th - 10, tw + 8, 10, NAVY)
    # flare stack with flame
    cv.fill(x + 268, y + 26, 12, h - 72, INK)
    cv.triangle(x + 262, y + 30, x + 286, y + 30, x + 274, y + 2, ORANGE)
    cv.triangle(x + 266, y + 30, x + 282, y + 30, x + 274, y + 10, FLAME)
    cv.triangle(x + 256, y + 34, x + 292, y + 34, x + 274, y + 16, ORANGE)
    # oil barrel
    cv.fill(x + w - 74, y + h - 92, 52, 46, INK)
    cv.fill(x + w - 70, y + h - 88, 44, 38, (31, 41, 55))
    cv.hline(x + w - 70, y + h - 76, 44, GOLD, 3)
    cv.hline(x + w - 70, y + h - 60, 44, GOLD, 3)
    # price tag
    cv.fill(x + 16, y + h - 118, 168, 52, WHITE)
    cv.rect(x + 16, y + h - 118, 168, 52, RED, 3)
    cv.text(x + 28, y + h - 110, "BRENT", 2, RED)
    cv.text(x + 28, y + h - 88, "$94.61", 3, INK)
    # rising arrow
    cv.line(x + 150, y + h - 74, x + 172, y + h - 104, RED)
    cv.line(x + 172, y + h - 104, x + 160, y + h - 102, RED)
    cv.line(x + 172, y + h - 104, x + 170, y + h - 92, RED)


def draw_ship_globe(cv, x, y, w, h):
    """Globe above a container ship on waves (trade / tariffs). Fits its box."""
    cv.fill(x, y, w, h, SKY)
    cx, cy, r = x + 64, y + 32, 28
    cv.circle(cx, cy, r, TEAL)
    cv.circle(cx, cy, r, INK, fill=False)
    cv.circle(cx - 10, cy - 5, 8, GREEN)
    cv.circle(cx + 9, cy + 8, 7, GREEN)
    cv.circle(cx + 4, cy - 13, 5, GREEN)
    cv.hline(cx - r + 4, cy - 10, 2 * r - 8, WHITE, 2)
    cv.hline(cx - r + 4, cy + 10, 2 * r - 8, WHITE, 2)
    # tariff stamp, top right
    cv.fill(x + w - 132, y + 8, 120, 30, WHITE)
    cv.rect(x + w - 132, y + 8, 120, 30, RED, 3)
    cv.text(x + w - 124, y + 15, "UP TO 15%", 2, RED)
    # sea
    cv.fill(x, y + h - 26, w, 26, (30, 64, 120))
    for wx in range(x + 8, x + w - 8, 30):
        cv.line(wx, y + h - 12, wx + 10, y + h - 16, WHITE)
    # containers + hull
    cols = [NAVY_LT, GOLD, TEAL, (180, 83, 9)]
    for i, cc in enumerate(cols):
        cv.fill(x + 150 + i * 52, y + h - 52, 46, 26, cc)
        cv.rect(x + 150 + i * 52, y + h - 52, 46, 26, INK, 2)
    cv.triangle(x + 130, y + h - 26, x + w - 20, y + h - 26,
                x + w - 44, y + h - 6, INK)
    cv.fill(x + 130, y + h - 26, w - 150, 18, RED)
    cv.rect(x + 130, y + h - 26, w - 150, 18, INK, 2)


def draw_missile(cv, x, y, w, h):
    """Missile on a launcher under a dark sky with stars. Fits its box."""
    cv.fill(x, y, w, h, (15, 23, 42))
    for sx, sy in ((x + 24, y + 14), (x + 70, y + 26), (x + 300, y + 16),
                   (x + 350, y + 30), (x + 110, y + 10), (x + 420, y + 22)):
        cv.fill(sx, sy, 4, 4, WHITE)
    # ground
    cv.fill(x, y + h - 12, w, 12, (51, 65, 85))
    # launcher rails
    cv.line(x + 150, y + h - 12, x + 200, y + 34, INK)
    cv.line(x + 156, y + h - 12, x + 206, y + 34, INK)
    cv.fill(x + 138, y + h - 16, 84, 6, INK)
    # missile body
    cv.fill(x + 198, y + 8, 20, 42, (226, 232, 240))
    cv.rect(x + 198, y + 8, 20, 42, INK, 2)
    cv.triangle(x + 198, y + 12, x + 218, y + 12, x + 208, y + 2, RED)
    cv.fill(x + 198, y + 34, 20, 10, RED)
    # fins
    cv.triangle(x + 198, y + 42, x + 184, y + 58, x + 198, y + 54, RED)
    cv.triangle(x + 218, y + 42, x + 232, y + 58, x + 218, y + 54, RED)
    # exhaust glow
    cv.triangle(x + 201, y + 50, x + 215, y + 50, x + 208, y + 66, FLAME)
    cv.triangle(x + 204, y + 50, x + 212, y + 50, x + 208, y + 60, ORANGE)
    # warning label, bottom right
    cv.fill(x + w - 150, y + h - 44, 136, 34, GOLD)
    cv.rect(x + w - 150, y + h - 44, 136, 34, INK, 2)
    cv.text(x + w - 140, y + h - 40, "TACTICAL", 2, INK)
    cv.text(x + w - 140, y + h - 24, "NUCLEAR", 2, INK)


def draw_gaza(cv, x, y, w, h):
    """City skyline at dusk with a warning triangle (Gaza strike). Fits box."""
    cv.fill(x, y, w, h, (254, 226, 226))
    cv.fill(x, y + h - 12, w, 12, (120, 53, 15))
    for bx, bw, bh in ((x + 10, 44, 26), (x + 62, 36, 34),
                       (x + 106, 40, 22), (x + 154, 30, 30),
                       (x + 192, 42, 24), (x + 240, 34, 32)):
        cv.fill(bx, y + h - 12 - bh, bw, bh, (68, 64, 60))
        cv.rect(bx, y + h - 12 - bh, bw, bh, INK, 2)
    cx = x + w // 2
    cv.triangle(cx - 20, y + 4, cx + 20, y + 4, cx, y + 34, GOLD)
    cv.text(cx - 3, y + 12, "!", 1, INK)


def draw_ukraine(cv, x, y, w, h):
    """Burning refinery silhouette at night (Ukraine strikes). Fits box."""
    cv.fill(x, y, w, h, (15, 23, 42))
    for sx, sy in ((x + 22, y + 8), (x + 70, y + 14), (x + 200, y + 8),
                   (x + 250, y + 16)):
        cv.fill(sx, sy, 3, 3, WHITE)
    cv.fill(x, y + h - 10, w, 10, (51, 65, 85))
    for tx, tw, th in ((x + 16, 46, 22), (x + 74, 38, 30)):
        cv.fill(tx, y + h - 10 - th, tw, th, (30, 41, 59))
        cv.rect(tx, y + h - 10 - th, tw, th, INK, 2)
    cv.fill(x + 126, y + 18, 8, h - 28, INK)
    cv.triangle(x + 121, y + 20, x + 139, y + 20, x + 130, y + 4, ORANGE)
    cv.triangle(x + 124, y + 20, x + 136, y + 20, x + 130, y + 10, FLAME)
    cv.triangle(x + 160, y + 34, x + 196, y + 34, x + 178, y + 8, ORANGE)
    cv.triangle(x + 167, y + 34, x + 189, y + 34, x + 178, y + 18, FLAME)


def draw_rocket(cv, x, y, w, h):
    """Rocket climbing past stars toward a small station (space). Fits box."""
    cv.fill(x, y, w, h, (12, 24, 48))
    for sx, sy in ((x + 20, y + 8), (x + 60, y + 20), (x + 210, y + 10),
                   (x + 250, y + 24), (x + 40, y + 38), (x + 230, y + 40)):
        cv.fill(sx, sy, 3, 3, WHITE)
    # planet, top right
    cv.circle(x + w - 30, y + 12, 10, TEAL)
    cv.line(x + w - 44, y + 8, x + w - 16, y + 16, GOLD)
    # rocket body
    rx = x + w // 2 - 9
    cv.fill(rx, y + 10, 18, 24, WHITE)
    cv.rect(rx, y + 10, 18, 24, INK, 2)
    cv.triangle(rx, y + 10, rx + 18, y + 10, rx + 9, y + 2, RED)
    cv.fill(rx, y + 22, 18, 6, TEAL)
    cv.triangle(rx, y + 34, rx - 10, y + 44, rx, y + 40, RED)
    cv.triangle(rx + 18, y + 34, rx + 28, y + 44, rx + 18, y + 40, RED)
    cv.triangle(rx + 3, y + 34, rx + 15, y + 34, rx + 9, y + 48, FLAME)
    cv.triangle(rx + 6, y + 34, rx + 12, y + 34, rx + 9, y + 42, ORANGE)
    # station ring, bottom left
    cv.circle(x + 26, y + h - 12, 8, GOLD_LT, fill=False)
    cv.fill(x + 22, y + h - 13, 8, 3, GOLD)


# ------------------------------------------------------------- layout -------
def panel(cv, x, y, w, h):
    cv.fill(x, y, w, h, WHITE)
    cv.rect(x, y, w, h, INK, 2)


def kicker(cv, x, y, s, c=RED):
    cv.text(x, y, s, 2, c)
    return y + 20


def headline(cv, x, y, lines, scale, c=INK):
    for ln in lines:
        cv.text(x, y, ln, scale, c)
        y += 7 * scale + 4
    return y


def body(cv, x, y, s, max_w, scale=2, c=(51, 51, 51)):
    for ln in cv.wrap(s, max_w, scale):
        cv.text(x, y, ln, scale, c)
        y += 7 * scale + 5
    return y


def draw_page():
    cv = Canvas(W, H, PAPER)

    # ---- masthead ------------------------------------------------------
    cv.fill(24, 20, 976, 96, NAVY)
    cv.rect(24, 20, 976, 96, INK, 2)
    title = "THE WORLD TODAY"
    tw = cv.text_w(title, 6)
    cv.text(24 + (976 - tw) // 2, 34, title, 6, WHITE)
    sub = "WORLD NEWS IN ONE IMAGE"
    sw = cv.text_w(sub, 2)
    cv.text(24 + (976 - sw) // 2, 88, sub, 2, GOLD_LT)

    # ---- date bar ------------------------------------------------------
    cv.fill(24, 124, 976, 46, GOLD)
    cv.rect(24, 124, 976, 46, INK, 2)
    date = "THURSDAY  26 NOVEMBER 2026"
    dw = cv.text_w(date, 4)
    cv.text(24 + (976 - dw) // 2, 135, date, 4, INK)

    # ---- lead story ----------------------------------------------------
    panel(cv, 24, 182, 976, 268)
    lx, ly = 44, 198
    ly = kicker(cv, lx, ly, "MIDDLE EAST  -  ENERGY")
    ly = headline(cv, lx, ly + 6, ["HOUTHIS HIT", "SAUDI REFINERY"], 4)
    ly = body(cv, lx, ly + 8,
              "Yemen's Houthis claim strikes on Ras Tanura, the kingdom's "
              "largest refinery, and on Riyadh. Brent crude jumps past $94 "
              "a barrel as markets fear supply disruption.",
              560, 2)
    draw_refinery(cv, 640, 198, 340, 236)

    # ---- row 2: tariffs + nukes ---------------------------------------
    panel(cv, 24, 462, 482, 232)
    ax, ay = 40, 476
    ay = kicker(cv, ax, ay, "TRADE  -  USA")
    ay = headline(cv, ax, ay + 4, ["US TARIFFS HIT", "14 NATIONS"], 3)
    body(cv, ax, ay + 6,
         "Washington proposes duties up to 15% on 14 partners. Markets "
         "slide.",
         450, 2)
    draw_ship_globe(cv, 40, 600, 450, 86)

    panel(cv, 518, 462, 482, 232)
    bx, by = 534, 476
    by = kicker(cv, bx, by, "SECURITY  -  KOREA")
    by = headline(cv, bx, by + 4, ["KIM ORDERS MORE", "TACTICAL NUKES"], 3)
    body(cv, bx, by + 6,
         "Kim calls for wider deployment of tactical nuclear arms, KCNA "
         "reports.",
         450, 2)
    draw_missile(cv, 534, 600, 450, 86)

    # ---- row 3: three stories -----------------------------------------
    cols = [
        (24, "GAZA", "GAZA STRIKE KILLS", "HAMAS OFFICIAL",
         "Israel kills colonel Abuelouf and his family; ceasefire under "
         "strain.", draw_gaza),
        (352, "UKRAINE", "UKRAINE HITS", "RUSSIAN REFINERIES",
         "Kyiv strikes two refineries overnight; Putin vows retaliation.",
         draw_ukraine),
        (680, "SPACE", "PAKISTAN'S FIRST", "ASTRONAUT",
         "Zeeshan Ali to fly China's Shenzhou-24 to the Tiangong station.",
         draw_rocket),
    ]
    for px, kick, h1, h2, txt, art in cols:
        panel(cv, px, 706, 320, 222)
        py = kicker(cv, px + 16, 718, kick)
        py = headline(cv, px + 16, py + 4, [h1, h2], 2)
        body(cv, px + 16, py + 6, txt, 288, 2)
        art(cv, px + 16, 862, 288, 52)

    # ---- briefs strip ---------------------------------------------------
    cv.fill(24, 940, 976, 64, NAVY)
    cv.rect(24, 940, 976, 64, INK, 2)
    cv.text(40, 950, "ALSO TODAY:", 2, GOLD_LT)
    body(cv, 40, 970,
         "Bangladesh garment wage +36%  -  N. Korea orders Swiss office "
         "shut  -  Lebanon to open 2nd airport  -  India marks "
         "Constitution Day",
         944, 2, WHITE)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    cv = draw_page()
    n = write_png(path, cv)
    print(f"wrote {path} ({cv.w}x{cv.h}, {n} bytes)")


if __name__ == "__main__":
    main()
