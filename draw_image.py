#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261120.

One image summing up the world news of Friday 20 November 2026:
six verified stories across regions and fields, drawn entirely in code
with PIL. No photos, no copied artwork.

Stories (each verified against at least two independent sources):
  1. Russian missiles land in Poland; NATO calls it a grave violation (AP, ISW)
  2. Global stocks plunge: S&P 500 -3.7%, Nikkei -5.1% (One Turn, Morningstar)
  3. Bitcoin falls below $60,000, first time since July (TheStreet, CryptoDisrupt)
  4. BepiColombo reaches Mercury after 8 years (The Guardian, Sky & Telescope)
  5. Magnitude 6.7 quake shakes central Peru (USGS via TBS News, earthquakelist)
  6. UK and EU seal new post-Brexit deals (The Guardian, One Turn)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- fonts
def find_font(names):
    for p in names:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("none of %r found" % (names,))


ANTON = find_font([
    "/home/hatch/.fonts/Anton-Regular.ttf",
    "/usr/share/fonts/truetype/anton/Anton-Regular.ttf",
])
NOTO_BOLD = find_font([
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
])
NOTO = find_font([
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
])


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- palette
PAPER = (245, 241, 232)
INK = (26, 32, 44)
SUB = (68, 64, 58)
NAVY = (16, 35, 63)
GOLD = (212, 172, 13)
CARD = (255, 255, 255)
CARD_EDGE = (217, 210, 194)

STORIES = [
    dict(
        kicker="SECURITY  ·  EUROPE",
        color=(176, 58, 46),
        tint=(253, 237, 236),
        headline="MISSILES LAND IN POLAND",
        sub="Two Russian missiles and a drone came down in Poland. NATO calls it a grave violation of its airspace.",
        icon="missile",
    ),
    dict(
        kicker="MARKETS  ·  GLOBAL",
        color=(26, 82, 118),
        tint=(235, 245, 251),
        headline="STOCKS PLUNGE WORLDWIDE",
        sub="The S&P 500 fell 3.7% into correction. Japan's Nikkei dropped 5.1% as AI shares sold off.",
        icon="chart",
    ),
    dict(
        kicker="CRYPTO",
        color=(185, 119, 14),
        tint=(254, 245, 231),
        headline="BITCOIN BELOW $60,000",
        sub="First time since July. More than $1 billion in leveraged positions was liquidated in 24 hours.",
        icon="bitcoin",
    ),
    dict(
        kicker="SPACE",
        color=(108, 52, 131),
        tint=(244, 236, 247),
        headline="BEPICOLOMBO REACHES MERCURY",
        sub="After 8 years and 6 billion miles, the European-Japanese probe arrives. Orbit entry on Saturday.",
        icon="mercury",
    ),
    dict(
        kicker="DISASTER  ·  PERU",
        color=(147, 81, 22),
        tint=(253, 242, 233),
        headline="6.7 QUAKE SHAKES PERU",
        sub="The tremor struck the central Andes at 7:09 p.m. and was felt in Lima. No casualties reported.",
        icon="quake",
    ),
    dict(
        kicker="DIPLOMACY  ·  EUROPE",
        color=(17, 120, 100),
        tint=(234, 250, 241),
        headline="UK AND EU SEAL NEW DEALS",
        sub="Food trade, carbon markets and youth mobility - the biggest Brexit reset step yet.",
        icon="deal",
    ),
]

# ---------------------------------------------------------------- helpers

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- icons
# Each draws a simple pictogram into a 96x96 RGBA layer.

def icon_missile(d):
    # flame
    d.polygon([(43, 72), (53, 72), (48, 90)], fill=(230, 126, 34))
    d.polygon([(45, 72), (51, 72), (48, 82)], fill=(241, 196, 15))
    # fins
    d.polygon([(40, 56), (27, 74), (40, 70)], fill=(44, 62, 80))
    d.polygon([(56, 56), (69, 74), (56, 70)], fill=(44, 62, 80))
    # body
    d.rounded_rectangle([40, 16, 56, 72], radius=6, fill=(93, 109, 126))
    # nose cone
    d.polygon([(40, 18), (56, 18), (48, 4)], fill=(176, 58, 46))
    # window
    d.ellipse([43, 30, 53, 40], fill=(174, 214, 241), outline=(44, 62, 80), width=2)


def icon_chart(d):
    # axes
    d.line([(14, 84), (14, 14)], fill=(44, 62, 80), width=4)
    d.line([(14, 84), (86, 84)], fill=(44, 62, 80), width=4)
    # falling line
    pts = [(20, 28), (33, 40), (45, 36), (58, 54), (70, 50), (82, 70)]
    d.line(pts, fill=(176, 58, 46), width=5, joint="curve")
    # arrowhead
    d.polygon([(82, 70), (70, 66), (78, 80)], fill=(176, 58, 46))


def icon_bitcoin(d):
    d.ellipse([8, 8, 88, 88], fill=(247, 147, 26), outline=(185, 106, 0), width=3)
    f = font(NOTO_BOLD, 56)
    d.text((48, 48), "B", font=f, fill=(255, 255, 255), anchor="mm")
    # two vertical strokes of the bitcoin sign
    d.rectangle([37, 20, 41, 76], fill=(255, 255, 255))
    d.rectangle([53, 20, 57, 76], fill=(255, 255, 255))


def icon_mercury(d):
    # planet with craters
    d.ellipse([10, 34, 66, 90], fill=(176, 169, 159), outline=(138, 131, 120), width=3)
    for (x, y, r) in [(26, 50, 6), (44, 66, 8), (30, 74, 4), (50, 46, 4)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(138, 131, 120))
    # spacecraft
    d.rectangle([56, 14, 62, 28], fill=(36, 113, 163))   # left panel
    d.rectangle([80, 14, 86, 28], fill=(36, 113, 163))   # right panel
    d.rectangle([62, 10, 80, 32], fill=(234, 242, 248), outline=(44, 62, 80), width=2)
    d.line([(71, 32), (60, 46)], fill=(44, 62, 80), width=2)


def icon_quake(d):
    pts = [(8, 62), (20, 62), (26, 34), (34, 62), (42, 62), (48, 24),
           (56, 62), (64, 62), (70, 46), (78, 62), (88, 62)]
    d.line(pts, fill=(146, 43, 33), width=4, joint="curve")
    d.line([(8, 78), (88, 78)], fill=(44, 62, 80), width=3)


def icon_deal(d):
    # document
    d.rounded_rectangle([20, 12, 68, 84], radius=4, fill=(255, 255, 255),
                        outline=(44, 62, 80), width=3)
    d.polygon([(56, 12), (68, 24), (56, 24)], fill=(213, 216, 220))
    for y in (36, 46, 56):
        d.line([(28, y), (52, y)], fill=(93, 109, 126), width=4)
    # wax seal
    d.ellipse([56, 60, 82, 86], fill=(176, 58, 46), outline=(146, 43, 33), width=2)
    d.polygon(star_points(69, 73, 7, 3), fill=(241, 196, 15))


ICONS = {
    "missile": icon_missile,
    "chart": icon_chart,
    "bitcoin": icon_bitcoin,
    "mercury": icon_mercury,
    "quake": icon_quake,
    "deal": icon_deal,
}


def draw_icon(base, cx, cy, name, tint, size=96):
    layer = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([2, 2, 94, 94], fill=tint + (255,))
    ICONS[name](d)
    if size != 96:
        layer = layer.resize((size, size), Image.LANCZOS)
    base.alpha_composite(layer, (cx - size // 2, cy - size // 2))


# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- header band
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 144, W, 148], fill=GOLD)
    f_kick = font(NOTO_BOLD, 22)
    d.text((28, 20), "THE WORLD IN ONE DAY", font=f_kick, fill=(232, 184, 75))
    f_date = font(ANTON, 68)
    d.text((28, 46), "20 NOVEMBER 2026", font=f_date, fill=(255, 255, 255))
    # FRIDAY tag, top right
    tag = "FRIDAY"
    f_tag = font(NOTO_BOLD, 26)
    tw = d.textlength(tag, font=f_tag)
    d.rounded_rectangle([W - 28 - tw - 36, 34, W - 28, 34 + 52], radius=10,
                        fill=(192, 57, 43))
    d.text((W - 28 - tw - 18, 60), tag, font=f_tag, fill=(255, 255, 255),
           anchor="lm")
    f_count = font(NOTO_BOLD, 22)
    d.text((W - 28, 116), "6 STORIES", font=f_count, fill=(232, 184, 75),
           anchor="ra")

    # ---- intro line
    f_intro = font(NOTO, 23)
    d.text((W // 2, 172), "Six stories that defined the day — war, markets, crypto, space, disaster, diplomacy",
           font=f_intro, fill=SUB, anchor="mm")

    # ---- grid of story cards
    margin, gutter = 28, 20
    col_w = (W - 2 * margin - gutter) // 2
    grid_top, grid_bottom = 204, 972
    row_h = (grid_bottom - grid_top - 2 * 18) // 3
    f_kicker = font(NOTO_BOLD, 19)
    f_head = font(ANTON, 31)
    f_sub = font(NOTO, 20)

    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (col_w + gutter)
        y0 = grid_top + row * (row_h + 18)
        x1, y1 = x0 + col_w, y0 + row_h

        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD,
                            outline=CARD_EDGE, width=2)
        # accent bar across the top of the card
        d.rounded_rectangle([x0, y0, x1, y0 + 7], radius=3, fill=s["color"])
        d.rectangle([x0, y0 + 4, x1, y0 + 7], fill=s["color"])

        # Measure text first so the content block can be vertically centred.
        tx = x0 + 122
        tw_text = x1 - 18 - tx
        head_lines = wrap(d, s["headline"], f_head, tw_text)[:2]
        sub_lines = wrap(d, s["sub"], f_sub, tw_text)[:3]
        content_h = 24 + 6 + 34 * len(head_lines) + 8 + 25 * len(sub_lines)
        top = y0 + (row_h - content_h) // 2

        # icon disc, left, centred on the kicker + headline zone
        draw_icon(img, x0 + 64, top + 28 + 17 * len(head_lines),
                  s["icon"], s["tint"], size=104)

        # kicker
        d.text((tx, top), s["kicker"], font=f_kicker, fill=s["color"])
        # headline
        hy = top + 28
        for ln in head_lines:
            d.text((tx, hy), ln, font=f_head, fill=INK)
            hy += 34
        # sub text
        sy = hy + 8
        for ln in sub_lines:
            d.text((tx, sy), ln, font=f_sub, fill=SUB)
            sy += 25

    # ---- footer
    f_foot = font(NOTO, 18)
    d.text((W // 2, 994),
           "All six events happened or were first reported on Friday, 20 November 2026.",
           font=f_foot, fill=SUB, anchor="mm")

    img.convert("RGB").save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
