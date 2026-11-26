#!/usr/bin/env python3
"""Build-time renderer for THE WEDNESDAY GAZETTE (news-image-20261125).

Draws entry.png (1024x1024) with PIL. Build-time only: the submitted
main.py is stdlib-only and never imports PIL.
All facts come from RESEARCH.md (news-image-20261125-lab).
Layout follows the winning skeleton: masthead + 3 lead banners +
12 illustrated tiles + market strip + world-map band + 2-column ALSO +
sources footer.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(BASE, "fonts")

PAPER = (248, 244, 233)
INK = (25, 25, 25)
INK_SOFT = (70, 70, 70)
RED = (158, 27, 27)
NAVY = (30, 58, 92)
TEAL = (38, 102, 102)
GOLD = (176, 132, 52)
RULE = (25, 25, 25)
OCEAN = (186, 214, 228)
LAND = (214, 200, 158)
LAND2 = (196, 186, 140)


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


SERIF = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANSB = "DejaVuSans-Bold.ttf"


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, max_w, leading, max_lines=None):
    """Draw wrapped text; returns y after last line."""
    lines = wrap(d, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def flame(d, cx, base_y, s, col1=(230, 90, 20), col2=(245, 180, 40)):
    """Simple flame: outer + inner triangle-ish teardrop."""
    d.polygon([(cx - s, base_y), (cx - s * 0.55, base_y - s * 1.5),
               (cx, base_y - s * 2.0), (cx + s * 0.55, base_y - s * 1.4),
               (cx + s, base_y)], fill=col1)
    d.polygon([(cx - s * 0.45, base_y), (cx - s * 0.25, base_y - s * 0.9),
               (cx, base_y - s * 1.2), (cx + s * 0.25, base_y - s * 0.8),
               (cx + s * 0.45, base_y)], fill=col2)


def smoke(d, cx, cy, s, col=(120, 120, 120)):
    for i, r in enumerate((s, s * 0.75, s * 0.55)):
        d.ellipse([cx - r + i * 3, cy - r - i * s, cx + r + i * 3,
                   cy + r - i * s], fill=col)


# ---------------------------------------------------------------- map data
# Simplified continent outlines as (lon, lat) points, equirectangular.
NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                 (-85, 80), (-80, 73), (-75, 72), (-65, 62), (-55, 52),
                 (-60, 47), (-70, 42), (-75, 35), (-80, 32), (-81, 26),
                 (-84, 30), (-90, 21), (-95, 19), (-97, 16), (-92, 15),
                 (-86, 13), (-83, 9), (-79, 9), (-85, 11), (-90, 14),
                 (-95, 16), (-100, 17), (-105, 20), (-110, 23), (-114, 29),
                 (-120, 34), (-125, 40), (-124, 48), (-130, 55), (-140, 60),
                 (-150, 61), (-158, 58), (-165, 60)]
SOUTH_AMERICA = [(-80, 10), (-77, 7), (-72, 12), (-64, 11), (-60, 9),
                 (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-40, -20),
                 (-48, -27), (-52, -33), (-58, -38), (-65, -41), (-68, -50),
                 (-70, -54), (-73, -50), (-73, -40), (-72, -30), (-70, -20),
                 (-77, -12), (-80, -6), (-81, 0), (-80, 5)]
AFRICA = [(-17, 15), (-17, 21), (-10, 31), (-5, 35), (0, 36), (10, 37),
          (20, 32), (30, 31), (32, 31), (35, 28), (37, 22), (40, 15),
          (43, 11), (48, 11), (51, 12), (46, 5), (41, 0), (40, -5),
          (36, -18), (33, -26), (28, -33), (20, -35), (17, -29), (14, -22),
          (12, -17), (13, -10), (9, -1), (9, 4), (0, 6), (-8, 5),
          (-13, 8), (-17, 12)]
EUROPE = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50),
          (0, 51), (3, 53), (7, 54), (8, 57), (10, 59), (5, 60), (5, 62),
          (12, 65), (18, 69), (25, 71), (30, 70), (40, 68), (45, 68),
          (50, 69), (55, 68), (60, 69), (65, 68), (68, 66), (60, 60),
          (55, 55), (50, 50), (45, 47), (40, 44), (35, 42), (30, 41),
          (28, 41), (26, 38), (23, 36), (20, 38), (18, 40), (15, 38),
          (12, 44), (8, 44), (3, 42), (0, 38), (-2, 37), (-6, 36), (-9, 37)]
ASIA = [(60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74),
        (120, 73), (130, 72), (140, 72), (150, 70), (160, 69), (170, 66),
        (178, 65), (170, 60), (162, 56), (158, 52), (150, 59), (142, 55),
        (140, 50), (135, 45), (130, 42), (127, 40), (126, 38), (122, 38),
        (120, 35), (118, 30), (112, 25), (108, 20), (105, 15), (103, 10),
        (100, 8), (98, 12), (95, 16), (92, 21), (90, 22), (88, 22),
        (85, 19), (80, 15), (77, 8), (75, 12), (72, 20), (70, 22),
        (66, 25), (62, 25), (58, 25), (55, 26), (52, 27), (50, 29),
        (48, 30), (50, 26), (54, 24), (56, 26), (58, 24), (59, 22),
        (57, 17), (55, 17), (52, 16), (48, 14), (44, 13), (43, 12),
        (40, 15), (39, 20), (38, 24), (36, 28), (35, 30), (34, 28),
        (35, 31), (36, 36), (40, 38), (42, 41), (45, 42), (48, 44),
        (50, 47), (52, 50), (55, 52), (58, 55), (60, 58), (62, 62),
        (65, 66), (68, 68)]
SUMATRA = [(95, 5), (98, 2), (102, -2), (105, -5), (104, -6), (100, 0), (96, 4)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3),
          (109, -1)]
JAVA = [(105, -6), (110, -7), (114, -8), (114, -9), (108, -8), (105, -7)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (145, -6), (147, -9),
              (143, -8), (138, -8), (132, -4)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 52), (1, 51),
      (-3, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
         (141, 41), (143, 42), (145, 44), (142, 44), (140, 40), (139, 36),
         (136, 35), (133, 34), (131, 33)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -25),
              (44, -25), (43, -20)]
CONTINENTS = [NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EUROPE, ASIA, SUMATRA,
              BORNEO, JAVA, NEW_GUINEA, AUSTRALIA, UK, JAPAN, MADAGASCAR]

# (number, label, lat, lon) — from RESEARCH.md section F
PINS = [
    (1, "Hormuz", 26.5, 56.3),
    (2, "Riyadh", 24.7, 46.7),
    (3, "Hodeidah", 14.8, 42.95),
    (4, "Ras Tanura", 26.65, 50.05),
    (5, "Brooklyn", 40.65, -73.95),
    (6, "New York", 40.7, -74.0),
    (7, "Jiuquan", 40.96, 100.3),
    (8, "Damazin", 11.77, 34.35),
    (9, "Gaza", 31.53, 34.45),
    (10, "Cikande", -6.2, 106.3),
    (11, "Cairo", 30.05, 31.25),
    (12, "Canberra", -35.28, 149.13),
]

# ------------------------------------------------------------- illustrations
def scene_gulf(d, x, y, w, h):
    """Night Gulf: dark sea, tan shore, tanker + flames at Hormuz,
    Riyadh tower, missile arcs."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 66))
    # stars
    for sx, sy in [(12, 10), (40, 22), (90, 8), (150, 16), (210, 10),
                   (260, 20), (300, 8), (60, 30), (180, 28)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 220, 200))
    # shore (Arabian peninsula hint, bottom right)
    d.polygon([(x + w * 0.55, y + h), (x + w * 0.62, y + h * 0.55),
               (x + w * 0.8, y + h * 0.62), (x + w, y + h * 0.5),
               (x + w, y + h)], fill=(196, 178, 140))
    # sea lanes
    for ly in (0.35, 0.55, 0.75):
        d.line([x + 8, y + h * ly, x + w - 8, y + h * ly],
               fill=(70, 110, 150), width=1)
    # tanker at Hormuz (left)
    tx, ty = x + w * 0.16, y + h * 0.62
    d.rectangle([tx, ty, tx + 62, ty + 12], fill=(60, 60, 60))
    d.rectangle([tx + 46, ty - 10, tx + 58, ty], fill=(90, 90, 90))
    flame(d, tx + 18, ty, 9)
    flame(d, tx + 44, ty, 7)
    smoke(d, tx + 30, ty - 22, 7, (150, 150, 150))
    # second tanker, small, mid
    tx2, ty2 = x + w * 0.42, y + h * 0.72
    d.rectangle([tx2, ty2, tx2 + 44, ty2 + 9], fill=(70, 70, 70))
    flame(d, tx2 + 12, ty2, 6)
    # Riyadh tower (right): tall needle tower
    bx = x + w * 0.82
    d.polygon([(bx - 12, y + h), (bx - 5, y + h * 0.18), (bx + 5, y + h * 0.18),
               (bx + 12, y + h)], fill=(120, 120, 130))
    d.ellipse([bx - 9, y + h * 0.30, bx + 9, y + h * 0.52], fill=(200, 170, 90))
    flame(d, bx, y + h * 0.55, 8)
    # missile arcs
    d.arc([x + w * 0.30, y - 6, x + w * 0.75, y + h * 0.5], 200, 340,
          fill=(245, 200, 60), width=2)
    d.arc([x + w * 0.05, y + h * 0.1, x + w * 0.5, y + h * 0.7], 300, 60,
          fill=(245, 200, 60), width=2)
    # labels
    lf = F(SANSB, 11)
    d.text((x + 8, y + 6), "HORMUZ", font=lf, fill=(255, 255, 255))
    d.text((x + w - 62, y + 6), "RIYADH", font=lf, fill=(255, 255, 255))
    d.text((x + w * 0.52, y + h - 18), "HODEIDAH", font=lf,
           fill=(255, 255, 255))


def scene_huawei(d, x, y, w, h):
    """Brooklyn courthouse facade + red GUILTY stamp."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    # sky
    d.rectangle([x, y, x + w, y + h * 0.42], fill=(168, 190, 214))
    # courthouse: pediment + columns
    cx = x + w // 2
    d.polygon([(cx - 110, y + h * 0.42), (cx, y + h * 0.12),
               (cx + 110, y + h * 0.42)], fill=(120, 110, 96))
    d.ellipse([cx - 12, y + h * 0.20, cx + 12, y + h * 0.36], fill=(200, 170, 90))
    for i in range(5):
        colx = cx - 96 + i * 48
        d.rectangle([colx, y + h * 0.44, colx + 16, y + h * 0.92],
                    fill=(245, 242, 232))
        d.rectangle([colx - 3, y + h * 0.42, colx + 19, y + h * 0.48],
                    fill=(220, 214, 198))
    d.rectangle([x, y + h * 0.92, x + w, y + h], fill=(90, 84, 74))
    # red stamp box
    sf = F(SANSB, 20)
    stamp = "GUILTY — 10 OF 12"
    tw = d.textlength(stamp, font=sf)
    sx, sy = cx - tw // 2 - 10, y + h * 0.58
    d.rectangle([sx, sy, sx + tw + 20, sy + 34], outline=RED, width=3,
                fill=(255, 255, 255))
    d.text((sx + 10, sy + 5), stamp, font=sf, fill=RED)


def scene_wallstreet(d, x, y, w, h):
    """Wild session: line plunges -1,100 then snaps back; towers below."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 46))
    # grid
    for gy in range(1, 5):
        yy = y + h * gy / 5
        d.line([x + 6, yy, x + w - 6, yy], fill=(50, 70, 100), width=1)
    # plunge then rebound
    pts = [(x + 10, y + h * 0.22), (x + w * 0.30, y + h * 0.34),
           (x + w * 0.52, y + h * 0.78), (x + w * 0.68, y + h * 0.62),
           (x + w * 0.84, y + h * 0.30), (x + w - 10, y + h * 0.26)]
    d.line(pts, fill=(245, 90, 60), width=4, joint="curve")
    d.line(pts, fill=(255, 210, 80), width=2, joint="curve")
    # dashed close line
    cy = y + h * 0.26
    for dx in range(0, w - 10, 14):
        d.line([x + 6 + dx, cy, x + 6 + dx + 8, cy], fill=(120, 200, 140),
               width=2)
    lf = F(SANSB, 11)
    d.text((x + w - 118, y + 8), "CLOSE +0.33%", font=lf,
           fill=(120, 220, 140))
    # towers
    for i, (tw, th) in enumerate([(26, 40), (20, 52), (30, 34), (18, 46)]):
        bx = x + 14 + i * 40
        d.rectangle([bx, y + h - th, bx + tw, y + h], fill=(40, 60, 90))
        for wy in range(3):
            d.rectangle([bx + 4, y + h - th + 6 + wy * 12, bx + tw - 4,
                         y + h - th + 10 + wy * 12], fill=(255, 210, 90))


def scene_generic(d, x, y, w, h, bg, kind):
    """Small tile scenes, drawn per story kind."""
    d.rectangle([x, y, x + w, y + h], fill=bg)
    cx, cy = x + w // 2, y + h // 2
    if kind == "cop31":
        # conference hall: rows of desks + flags + globe
        d.ellipse([cx - 16, y + 8, cx + 16, y + 40], fill=(70, 130, 170))
        d.arc([cx - 16, y + 8, cx + 16, y + 40], 0, 360, fill=(255, 255, 255),
              width=1)
        for r in range(3):
            yy = y + h - 14 - r * 9
            d.rectangle([x + 8, yy, x + w - 8, yy + 5], fill=(120, 110, 95))
        for i, col in enumerate([(60, 90, 160), (200, 60, 50), (60, 140, 90)]):
            fx = x + 16 + i * 24
            d.rectangle([fx, y + 12, fx + 14, y + 24], fill=col)
    elif kind == "rocket":
        # rocket on pad, flame, stars
        for sx, sy in [(8, 8), (w - 12, 14), (14, 26), (w - 20, 30)]:
            d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                      fill=(255, 255, 255))
        d.polygon([(cx - 8, y + 8), (cx + 8, y + 8), (cx + 5, y + h - 26),
                   (cx - 5, y + h - 26)], fill=(230, 230, 230))
        d.polygon([(cx, y + 2), (cx - 8, y + 10), (cx + 8, y + 10)],
                  fill=(200, 60, 50))
        d.rectangle([x + 8, y + h - 12, x + w - 8, y + h - 8],
                    fill=(90, 80, 70))
        flame(d, cx, y + h - 12, 7)
    elif kind == "tariffs":
        # crates with % tags
        for i, (bx, by, bw, bh) in enumerate([(8, 22, 26, 20), (38, 12, 26, 20),
                                              (68, 22, 26, 20), (22, 42, 26, 18),
                                              (56, 42, 26, 18)]):
            d.rectangle([x + bx, y + by, x + bx + bw, y + by + bh],
                        fill=(176, 132, 52), outline=(120, 85, 30))
            d.line([x + bx, y + by, x + bx + bw, y + by + bh],
                   fill=(120, 85, 30), width=1)
        d.text((x + w - 34, y + 4), "20%", font=F(SANSB, 12), fill=(255, 255, 255))
    elif kind == "drone":
        # drone silhouette over desert sun
        d.ellipse([x + w - 26, y + 6, x + w - 6, y + 26], fill=(245, 180, 60))
        d.rectangle([x + 6, y + h - 12, x + w - 6, y + h - 6], fill=(196, 164, 110))
        d.ellipse([cx - 14, cy - 8, cx + 14, cy + 8], fill=(50, 50, 55))
        d.line([cx - 26, cy - 10, cx + 26, cy - 10], fill=(50, 50, 55), width=3)
        d.line([cx - 26, cy + 10, cx + 26, cy + 10], fill=(50, 50, 55), width=3)
    elif kind == "gaza":
        # buildings + smoke
        for i, (bx, bh) in enumerate([(6, 30), (26, 44), (48, 26), (68, 38)]):
            d.rectangle([x + bx, y + h - bh, x + bx + 18, y + h],
                        fill=(140, 130, 115))
            d.rectangle([x + bx + 4, y + h - bh + 6, x + bx + 8,
                         y + h - bh + 10], fill=(60, 60, 60))
        smoke(d, cx + 10, y + 14, 8, (110, 110, 110))
    elif kind == "factory":
        # factory + flames + smoke
        d.rectangle([x + 6, y + h - 26, x + w - 6, y + h], fill=(110, 100, 88))
        d.rectangle([x + 12, y + 8, x + 20, y + h - 26], fill=(90, 82, 72))
        d.rectangle([x + 30, y + 16, x + 38, y + h - 26], fill=(90, 82, 72))
        flame(d, cx - 12, y + h - 26, 9)
        flame(d, cx + 16, y + h - 26, 7)
        smoke(d, cx, y + 12, 8, (120, 120, 120))
    elif kind == "bottle":
        # bottles + warning triangle
        for i in range(3):
            bx = x + 12 + i * 22
            d.rectangle([bx, y + 22, bx + 12, y + h - 8], fill=(40, 120, 80))
            d.rectangle([bx + 3, y + 14, bx + 9, y + 22], fill=(30, 90, 60))
        d.polygon([(x + w - 26, y + 8), (x + w - 8, y + 30), (x + w - 40, y + 30)],
                  fill=(245, 200, 40), outline=(200, 40, 30))
        d.text((x + w - 28, y + 14), "!", font=F(SANSB, 14), fill=(160, 20, 20))
    elif kind == "tanker":
        # overturned tanker truck + flames
        d.rectangle([x + 10, y + h - 22, x + w - 10, y + h - 14],
                    fill=(60, 60, 60))
        d.ellipse([x + 16, y + h - 30, x + 60, y + h - 12], fill=(180, 60, 40))
        d.rectangle([x + 62, y + h - 26, x + w - 14, y + h - 12],
                    fill=(120, 120, 120))
        flame(d, cx - 8, y + h - 22, 8)
        flame(d, cx + 18, y + h - 22, 6)
        smoke(d, cx, y + 10, 7, (110, 110, 110))
    elif kind == "scales":
        # scales of justice
        d.line([cx, y + 8, cx, y + h - 8], fill=(80, 70, 55), width=3)
        d.line([cx - 22, y + 12, cx + 22, y + 12], fill=(80, 70, 55), width=3)
        for s in (-1, 1):
            d.line([cx + s * 22, y + 12, cx + s * 16, y + 30],
                   fill=(80, 70, 55), width=2)
            d.arc([cx + s * 16 - 9, y + 24, cx + s * 16 + 9, y + 42], 0, 180,
                  fill=(176, 132, 52), width=3)
        d.ellipse([cx - 14, y + h - 10, cx + 14, y + h - 4], fill=(80, 70, 55))
    elif kind == "island":
        # island + palm + flag
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 130, 170))
        d.ellipse([cx - 34, y + h - 26, cx + 34, y + h - 10], fill=(214, 196, 140))
        d.line([cx, y + h - 24, cx, y + 12], fill=(110, 80, 40), width=3)
        for a in (-40, -10, 20, 50):
            import math
            ang = math.radians(a)
            d.line([cx, y + 14, cx + 18 * math.cos(ang),
                    y + 14 + 10 * math.sin(ang)], fill=(40, 130, 60), width=2)
        d.rectangle([cx, y + 12, cx + 16, y + 22], fill=(200, 60, 50))
    elif kind == "laptop":
        # laptop + lock + network nodes
        d.rectangle([x + 14, y + 12, x + w - 14, y + h - 20], fill=(40, 50, 66))
        d.rectangle([x + 18, y + 16, x + w - 18, y + h - 24], fill=(120, 190, 210))
        d.rectangle([x + 8, y + h - 20, x + w - 8, y + h - 14], fill=(70, 75, 85))
        d.ellipse([cx - 7, cy - 4, cx + 7, cy + 10], fill=(200, 60, 50))
        d.rectangle([cx - 5, cy - 12, cx + 5, cy - 2], outline=(200, 60, 50),
                    width=2)
    elif kind == "ship":
        # warship at sea + drone
        d.rectangle([x, y + h - 18, x + w, y + h], fill=(70, 110, 150))
        d.polygon([(x + 14, y + h - 18), (x + 80, y + h - 18),
                   (x + 72, y + h - 34), (x + 22, y + h - 34)],
                  fill=(90, 90, 95))
        d.rectangle([x + 40, y + h - 48, x + 46, y + h - 34], fill=(70, 70, 75))
        d.ellipse([cx + 8, y + 10, cx + 20, y + 18], fill=(50, 50, 55))
        d.line([cx, y + 14, cx + 28, y + 14], fill=(50, 50, 55), width=2)
        d.line([cx + 14, y + 22, cx + 30, y + 40], fill=(245, 200, 60), width=1)


# ---------------------------------------------------------------- map band
def draw_map(d, x, y, w, h):
    """Equirectangular world map, genuinely proportioned (lat range
    -60..84 mapped to the box height with a mild vertical stretch)."""
    d.rectangle([x, y, x + w, y + h], fill=OCEAN)
    # graticule
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360 * w
        d.line([gx, y, gx, y + h], fill=(160, 190, 208), width=1)
    for lat in (-30, 0, 30, 60):
        gy = y + (84 - lat) / 144 * h
        d.line([x, gy, x + w, gy], fill=(160, 190, 208), width=1)

    def px(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (84 - lat) / 144 * h)

    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(150, 138, 100))
    # equator label
    d.text((x + 4, y + (84 - 0) / 144 * h - 12), "EQUATOR",
           font=F(SANS, 8), fill=(110, 140, 165))
    # pins (5/6 Brooklyn vs New York nearly coincide: offset markers)
    offsets = {5: (-15, -8), 6: (13, 5)}
    for num, label, lat, lon in PINS:
        px_, py_ = px(lon, lat)
        ox, oy = offsets.get(num, (0, 0))
        mx, my = px_ + ox, py_ + oy
        if (ox, oy) != (0, 0):
            d.line([px_, py_, mx, my], fill=RED, width=1)
            d.ellipse([px_ - 2, py_ - 2, px_ + 2, py_ + 2], fill=RED)
        d.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        nf = F(SANSB, 9)
        tw = d.textlength(str(num), font=nf)
        d.text((mx - tw / 2, my - 6), str(num), font=nf, fill=(255, 255, 255))
    return px

# ------------------------------------------------------------------- content
LEADS = [
    ("scene_gulf", "THE GULF WAR — DAY 11: HORMUZ, RIYADH, HODEIDAH",
     "IRGC CLAIMS 2 tankers hit in Hormuz • Houthi missile hits Riyadh "
     "tower, 11 hurt • Coalition strikes Hodeidah",
     "IRGC CLAIMS"),
    ("scene_huawei", "HUAWEI GUILTY — 10 OF 12 COUNTS",
     "Bank fraud, sanctions, trade-secret theft • 11-week trial, 60+ "
     "witnesses • Sentencing 14 Sep 2027",
     "VERDICT TUE (US) • REPORTED WED"),
    ("scene_wallstreet", "WALL STREET'S WILD WEDNESDAY",
     "Dow -1,100 intraday, then back • Nvidia -3.9% to $149.30 • "
     "Hot core PCE 3.3",
     "WED 25 NOV CLOSE"),
]

# (num, kicker, headline, sub, scene, bg)
TILES = [
    (4, "CLIMATE • ANTALYA", "COP31 AFTERMATH: OPEC BLAMES EU, POPE LAMENTS FAILURE",
     "Collapse was Sun 22 Nov • 32+ nations reject Antalya Pact", "cop31",
     (226, 220, 200)),
    (5, "SPACE • JIUQUAN", "SHENZHOU-24 LIFTS OFF — FIRST PAKISTANI IN ORBIT",
     "Docked with Tiangong in 3.5 hrs • Crew of 3, home in a week", "rocket",
     (20, 30, 55)),
    (6, "TRADE • WASHINGTON", "NEW US TARIFFS FOR 14 PARTNERS",
     "China 20% • Europe 15% • Not before 25 Jan hearing", "tariffs",
     (240, 232, 210)),
    (7, "WAR • SUDAN", "RSF DRONE STRIKE KILLS 19 IN DAMAZIN",
     "Blue Nile • 20 hurt • 6 women among the dead", "drone",
     (232, 214, 170)),
    (8, "WAR • GAZA", "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
     "Shati camp • Chief, wife + 2 daughters • 6 hurt", "gaza",
     (228, 222, 208)),
    (9, "DISASTER • INDONESIA", "CIKANDE FIRE: 26 BODY BAGS, 28 STILL MISSING",
     "Search resumes • DNA tests take 2–3 weeks", "factory",
     (235, 228, 210)),
    (10, "HEALTH • INDIA", "TOXIC ALCOHOL DEATH TOLL NOW 20",
     "1,236 screened • 81 in hospital • 9 arrested", "bottle",
     (220, 232, 222)),
    (11, "DISASTER • EGYPT", "CAIRO TANKER FIRE: AT LEAST 31 DEAD",
     "Ring Road, Warraq • 21 hurt • 27 vehicles burned", "tanker",
     (240, 226, 210)),
    (12, "LAW • JERUSALEM", "JUDGE RECOMMENDS DROPPING TOP NETANYAHU CHARGE",
     "Case 4000 • Prosecutor to decide • 'Trial must end'", "scales",
     (228, 224, 212)),
    (13, "DIPLOMACY • PACIFIC", "SOLOMONS: NO FOREIGN MILITARY BASES",
     "Australia top security partner • China pact void", "island",
     (210, 228, 228)),
    (14, "CYBER • USA", "CIA/ODNI OSINT NETWORK HACKED",
     "Unclassified network only • No classified systems hit", "laptop",
     (222, 228, 236)),
    (15, "WAR • UKRAINE / LIBYA", "ODESA HIT: 2 DEAD; DRONE STRIKES RUSSIAN WARSHIP",
     "Off Libya • 2 Libyan officers killed • LNA vows revenge", "ship",
     (218, 228, 236)),
]

ALSO_LEFT = [
    (17, "Cricket: India–NZ Test 1 ends in a draw (23 Nov)"),
    (18, "Bangladesh raises garment minimum wage 36% to $139"),
    (19, "Venezuela reveals $237.5bn debt ahead of restructuring"),
    (20, "Shanghai party chief faces corruption probe"),
    (21, "Malaysia to return thousands of refugees to Myanmar"),
    (22, "Global landmine casualties hit five-year high"),
    (23, "WHO chief urges end to US fuel blockade on Cuba"),
    (24, "Sarkozy + Bruni to face witness-tampering trial"),
    (25, "Trump: US war funding vs Iran safe until January"),
    (26, "US DOJ charges 800+ in 400 global fraud cases"),
    (27, "Coast Guard finds 6 bodies from Cessna crash"),
    (28, "Jannik Sinner has knee surgery, out long-term"),
]
ALSO_RIGHT = [
    (29, "Lakers beat Jazz — Dončić 28 pts, 8 ast"),
    (30, "One year on from Hong Kong fire (168 dead), survivors mourn"),
    (31, "Museum of London reopens in restored Victorian market"),
    (32, "Japan data-centre boom faces local backlash"),
    (33, "Canada foreign-student curbs test Carney"),
    (34, "Duran Duran guitarist Andy Taylor dies, 65"),
    (35, "Jolie + Pitt settle French winery legal dispute"),
    (36, "Macy's Thanksgiving parade delayed by bad weather"),
    (37, "North Korea expels Swiss diplomat in sanctions row"),
    (38, "US Army blast of Iowa lead explosives 'huge success'"),
    (39, "US approves SpaceX plan for a million data satellites"),
    (40, "Russia's own figures show ~500,000 war dead in Ukraine"),
]

PIN_INDEX = [
    (1, "Hormuz", "IRGC claims 2 tankers hit"),
    (2, "Riyadh", "Houthi missile, 11 hurt"),
    (3, "Hodeidah", "Coalition strikes back"),
    (4, "Ras Tanura", "4 drones shot down"),
    (5, "Brooklyn", "Huawei guilty verdict"),
    (6, "New York", "Wall Street wild session"),
    (7, "Jiuquan", "Shenzhou-24 launches"),
    (8, "Damazin", "RSF drone strike, 19 dead"),
    (9, "Gaza", "Hamas security chief killed"),
    (10, "Cikande", "Factory fire, 28 missing"),
    (11, "Cairo", "Tanker fire, at least 31 dead"),
    (12, "Canberra", "Solomons security pact"),
]


# ------------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title = "THE WEDNESDAY GAZETTE"
    tf = F(SERIF, 42)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 8), title, font=tf, fill=INK)
    df = F(SANSB, 15)
    d.text((8, 56), "WEDNESDAY 25 NOVEMBER 2026", font=df, fill=INK)
    right = "40 STORIES • 4 CONTINENTS"
    d.text((W - 8 - d.textlength(right, font=df), 56), right, font=df, fill=INK)
    d.line([8, 76, W - 8, 76], fill=RULE, width=2)
    d.line([8, 79, W - 8, 79], fill=RULE, width=1)

    # ---- 3 lead banners
    lead_w, lead_gap = 330, 8
    scenes = {"scene_gulf": scene_gulf, "scene_huawei": scene_huawei,
              "scene_wallstreet": scene_wallstreet}
    for i, (scene, headline, sub, stamp) in enumerate(LEADS):
        x = 8 + i * (lead_w + lead_gap)
        y = 82
        scenes[scene](d, x, y, lead_w, 112)
        # stamp chip
        sf = F(SANSB, 10)
        sw = d.textlength(stamp, font=sf)
        d.rectangle([x, y, x + sw + 12, y + 18], fill=RED)
        d.text((x + 6, y + 3), stamp, font=sf, fill=(255, 255, 255))
        hy = text_block(d, x, y + 118, headline, F(SANSB, 15), INK,
                        lead_w, 18, max_lines=2)
        text_block(d, x, hy + 2, sub, F(SANS, 10), INK_SOFT, lead_w, 13,
                   max_lines=2)
        d.line([x, 268, x + lead_w, 268], fill=(180, 170, 150), width=1)

    # ---- 12 tiles (3 rows x 4)
    tile_w, tile_h, tgap = 247, 100, 6
    for idx, (num, kicker, headline, sub, kind, bg) in enumerate(TILES):
        row, col = divmod(idx, 4)
        x = 8 + col * (tile_w + tgap)
        y = 272 + row * (tile_h + 3)
        d.rectangle([x, y, x + tile_w, y + tile_h], fill=(255, 255, 255),
                    outline=(200, 190, 170))
        # illustration, left
        scene_generic(d, x + 1, y + 1, 86, tile_h - 2, bg, kind)
        # number badge on illustration
        nf = F(SANSB, 10)
        d.ellipse([x + 5, y + 5, x + 21, y + 21], fill=RED)
        ntw = d.textlength(str(num), font=nf)
        d.text((x + 13 - ntw / 2, y + 7), str(num), font=nf,
               fill=(255, 255, 255))
        tx = x + 94
        tw_ = tile_w - 94 - 6
        d.text((tx, y + 5), f"{num} • {kicker}", font=F(SANSB, 9), fill=RED)
        hy = text_block(d, tx, y + 20, headline, F(SANSB, 12), INK, tw_, 14,
                        max_lines=3)
        text_block(d, tx, hy + 1, sub, F(SANS, 9), INK_SOFT, tw_, 11,
                   max_lines=2)

    # ---- market strip
    my = 580
    d.rectangle([8, my, W - 8, my + 46], fill=NAVY)
    mf = F(SANSB, 12)
    mkt1 = ("MARKETS — WED 25 NOV CLOSE   DOW +0.33% 50,182.95  •  "
            "S&P -0.25% 7,182.78  •  NASDAQ -0.62% 23,585.80  •  "
            "NVIDIA -3.9% $149.30")
    mkt2 = ("BITCOIN — WED 25 NOV: DIP BELOW $59K, BACK ABOVE $60K  •  "
            "BRENT $94.61  •  GOLD FUT $3,535.80  •  ANT $82.79 +1.07%")
    d.text((16, my + 5), mkt1, font=mf, fill=(255, 255, 255))
    d.text((16, my + 25), mkt2, font=mf, fill=(255, 214, 120))

    # ---- map band
    d.text((8, 632), "WHERE IT HAPPENED", font=F(SANSB, 14), fill=INK)
    d.text((420, 632), "12 PINS — 4 CONTINENTS",
           font=F(SANSB, 14), fill=INK)
    draw_map(d, 8, 652, 400, 164)
    # pin index, two columns
    for i, (num, place, desc) in enumerate(PIN_INDEX):
        col = i // 6
        row = i % 6
        px_ = 420 + col * 300
        py_ = 654 + row * 27
        d.ellipse([px_, py_, px_ + 16, py_ + 16], fill=RED)
        nf = F(SANSB, 9)
        ntw = d.textlength(str(num), font=nf)
        d.text((px_ + 8 - ntw / 2, py_ + 3), str(num), font=nf,
               fill=(255, 255, 255))
        d.text((px_ + 22, py_ + 1), place, font=F(SANSB, 11), fill=INK)
        d.text((px_ + 22, py_ + 13), desc, font=F(SANS, 9), fill=INK_SOFT)
    d.text((420, 654 + 6 * 27 + 2),
           "ASIA 7  •  NORTH AMERICA 2  •  AFRICA 2  •  OCEANIA 1",
           font=F(SANSB, 10), fill=NAVY)

    # ---- ALSO, 2 columns
    d.text((8, 822), "ALSO — IN BRIEF", font=F(SANSB, 13), fill=INK)
    d.line([8, 840, W - 8, 840], fill=RULE, width=1)
    af = F(SANS, 9)
    afb = F(SANSB, 9)
    for col, items in enumerate((ALSO_LEFT, ALSO_RIGHT)):
        ax = 8 + col * 508
        ay = 844
        for num, text in items:
            d.text((ax, ay), f"{num}.", font=afb, fill=RED)
            d.text((ax + 22, ay), text, font=af, fill=INK)
            ay += 11

    # ---- footer
    d.line([8, 986, W - 8, 986], fill=RULE, width=1)
    foot = ("SOURCES: BBC • Reuters • Channel News Asia • Bloomberg • AP • CNN • "
            "The Motley Fool • Barchart • Investopedia • Finnhub • Morningstar — "
            "plus official releases (USTR, Saudi Civil Defense, Egypt Health "
            "Ministry, Emergency Lawyers, IDF). Claims marked CLAIMS are "
            "unconfirmed. All stories verified 25 November 2026.")
    text_block(d, 8, 991, foot, F(SANS, 9), INK_SOFT, W - 16, 12)

    out = os.path.join(BASE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
