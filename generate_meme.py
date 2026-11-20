#!/usr/bin/env python3
"""Render 'VICE CITY COURIER - INVOICE #GTA6-2013' meme, 1200x675 PNG.
Pure PIL, deterministic: no randomness, no timestamps, no network.
Line items as data; total computed in code from cents."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1200, 675
BG = (250, 246, 239)      # warm off-white #FAF6EF
NAVY = (27, 42, 74)       # #1B2A4A
MAGENTA = (230, 0, 126)   # #E6007E
GREY = (110, 116, 130)
WHITE = (255, 255, 255)
LIGHT_LINE = (210, 204, 192)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# Line items: (description, date/detail, amount_cents)
ITEMS = [
    ("Waiting \u2014 13 years", "17 Sep 2013 to 19 Nov 2026", 131300),
    ("Trailer #1 rewatches x 1,337", "", 13370),
    ("Delay fee", "02 Feb 2022", 20220),
    ("Delay fee", "05 Dec 2023", 12050),
    ("Delay fee", "06 May 2025", 19050),
    ("Hype \u2014 non-refundable", "", 6610),
]

TOTAL_CENTS = sum(amount for _, _, amount in ITEMS)
assert TOTAL_CENTS == 202600, f"total mismatch: {TOTAL_CENTS} cents"


def money(cents):
    return f"${cents // 100:,}.{cents % 100:02d}"


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Thin frame
    d.rectangle([14, 14, W - 15, H - 15], outline=NAVY, width=2)

    ghost = Image.open(os.path.join(ASSETS, "ghost.png")).convert("RGBA")

    # ---- Header ----
    # Ghost ~100px tall on the left
    gh = ghost.resize((100, 100), Image.LANCZOS)
    d_x, d_y = 48, 38
    img.paste(gh, (d_x, d_y), gh)
    d.text((162, 62), "make.fun", font=font(FONT_BOLD, 58), fill=NAVY)

    # Right side: INVOICE + number + date
    f_inv = font(FONT_BOLD, 56)
    f_meta = font(FONT_REG, 22)
    inv_w = d.textlength("INVOICE", font=f_inv)
    d.text((W - 48 - inv_w, 40), "INVOICE", font=f_inv, fill=NAVY)
    for i, line in enumerate(("No. GTA6-2013-VC", "Date: 19 Nov 2026")):
        lw = d.textlength(line, font=f_meta)
        d.text((W - 48 - lw, 100 + i * 26), line, font=f_meta, fill=NAVY)

    # Divider under header
    d.line([(48, 152), (W - 48, 152)], fill=MAGENTA, width=3)

    # ---- Title ----
    d.text((48, 168), "GTA VI \u2014 13 YEARS IN THE MAKING",
           font=font(FONT_BOLD, 33), fill=NAVY)
    d.text((48, 208), "Billed to: every fan who waited since 2013",
           font=font(FONT_REG, 23), fill=GREY)

    # ---- Table header ----
    f_th = font(FONT_BOLD, 19)
    d.text((48, 242), "DESCRIPTION", font=f_th, fill=GREY)
    amt_w = d.textlength("AMOUNT", font=f_th)
    d.text((W - 48 - amt_w, 242), "AMOUNT", font=f_th, fill=GREY)
    d.line([(48, 268), (W - 48, 268)], fill=LIGHT_LINE, width=2)

    # ---- Line items ----
    f_desc = font(FONT_BOLD, 24)
    f_date = font(FONT_REG, 17)
    f_amt = font(FONT_BOLD, 24)
    y = 278
    ROW_H = 48
    for desc, date, cents in ITEMS:
        d.text((48, y), desc, font=f_desc, fill=NAVY)
        if date:
            d.text((48, y + 25), date, font=f_date, fill=GREY)
        a = money(cents)
        aw = d.textlength(a, font=f_amt)
        d.text((W - 48 - aw, y), a, font=f_amt, fill=NAVY)
        y += ROW_H
        if desc != ITEMS[-1][0]:
            d.line([(48, y - 2), (W - 48, y - 2)], fill=LIGHT_LINE, width=1)

    # ---- Total ----
    d.line([(48, y + 2), (W - 48, y + 2)], fill=NAVY, width=2)
    f_tot = font(FONT_BOLD, 30)
    f_tot_amt = font(FONT_BOLD, 34)
    d.text((48, y + 12), "TOTAL", font=f_tot, fill=NAVY)
    t = money(TOTAL_CENTS)
    tw = d.textlength(t, font=f_tot_amt)
    d.text((W - 48 - tw, y + 8), t, font=f_tot_amt, fill=MAGENTA)

    # ---- Footer: magenta band ----
    band_y0 = 622
    d.rectangle([14, band_y0, W - 15, H - 15], fill=MAGENTA)
    # Small ghost on a white chip so the mark stays unmistakable on magenta
    d.rounded_rectangle([44, band_y0 + 5, 96, band_y0 + 47], radius=8, fill=WHITE)
    small = ghost.resize((40, 40), Image.LANCZOS)
    img.paste(small, (49, band_y0 + 6), small)
    d.text((110, band_y0 + 10), "PAID IN FULL", font=font(FONT_BOLD, 28), fill=WHITE)
    f_foot = font(FONT_BOLD, 20)
    line = "PAID BY MY AI AGENT ON MAKE.FUN"
    lw = d.textlength(line, font=f_foot)
    d.text((W - 48 - lw, band_y0 + 15), line, font=f_foot, fill=WHITE)

    out = os.path.join(ASSETS, "meme.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} total={money(TOTAL_CENTS)}")


if __name__ == "__main__":
    main()
