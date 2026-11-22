#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme: a 'LEONIDA POST - PACKAGE DELAYED' official
notice document. Crisp PIL text (readable at 480px) + the make.fun ghost
(AI-generated on white, blends onto the white document card).
Output: meme.png 1024x1024."""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
REPO = "/home/hatch/workspace/makefun/gta6-meme-x-01/repo"
GHOST = f"{REPO}/media-generation-ghost-white-bg-0-5ef4a6ad-70fb-4fe7-b889-566bcf5a0a58.webp"
OUT = f"{REPO}/meme.png"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, sz)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# --- background: sunset gradient + sun + sparkles ---
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img, "RGBA")
stops = [(43, 16, 85), (194, 24, 91), (255, 138, 101)]
for y in range(H):
    f = y / H
    if f < 0.5:
        c = lerp(stops[0], stops[1], f / 0.5)
    else:
        c = lerp(stops[1], stops[2], (f - 0.5) / 0.5)
    d.line([(0, y), (W, y)], fill=c)
# sun disc
d.ellipse([W - 260, 60, W - 60, 260], fill=(255, 214, 140, 90))
# sparkles
for (x, y, r) in [(80, 120, 5), (150, 300, 4), (940, 420, 5), (60, 700, 4),
                  (960, 800, 5), (120, 950, 4), (900, 60, 4), (420, 40, 4)]:
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 160))

# --- document card with soft shadow ---
d.rounded_rectangle([64, 64, 976, 976], radius=30, fill=(0, 0, 0, 90))
d.rounded_rectangle([56, 56, 968, 968], radius=28, fill=(255, 255, 255, 255))
d = ImageDraw.Draw(img, "RGBA")

NAVY = (26, 26, 46, 255)
GRAY = (119, 119, 119, 255)
RED = (198, 40, 40, 255)
MAGENTA = (194, 24, 91, 255)

def center(y, s, fnt, fill):
    d.text((W // 2, y), s, font=fnt, fill=fill, anchor="ma")

# header
center(100, "LEONIDA POST", font(62), NAVY)
center(172, "VICE CITY BRANCH  •  TRACKING #GTA6-VI-4811", font(25), GRAY)
d.line([(110, 212), (914, 212)], fill=(220, 220, 220, 255), width=2)
# title
center(240, "PACKAGE DELAYED", font(84), RED)

# fields: label above value
fields = [
    ("PACKAGE", "Grand Theft Auto VI"),
    ("SHIPPED", "September 17, 2013"),
    ("STATUS", "In transit — 4,811 days"),
    ("DELIVERY ATTEMPTED", "Never."),
]
y = 372
for label, value in fields:
    d.text((110, y), label, font=font(24), fill=GRAY)
    d.text((110, y + 30), value, font=font(42), fill=NAVY)
    y += 108

# ghost (white bg blends onto the white card)
ghost = Image.open(GHOST).convert("RGB").resize((270, 270), Image.LANCZOS)
img.paste(ghost, (690, 365))

# divider
d.line([(110, 800), (914, 800)], fill=(220, 220, 220, 255), width=2)
# footer
center(828, "Paid by my AI agent's", font(34), NAVY)
center(872, "make.fun bounty winnings.", font(34), MAGENTA)
center(922, "— EST. 2013, STILL WAITING —", font(22), GRAY)

# rotated PAID IN FULL stamp, just below the ghost (like the ghost stamped it)
stamp = Image.new("RGBA", (320, 110), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([4, 4, 316, 106], radius=10, outline=(194, 24, 91, 255), width=5)
sd.rounded_rectangle([12, 12, 308, 98], radius=8, outline=(194, 24, 91, 255), width=2)
sd.text((160, 55), "PAID IN FULL", font=font(40), fill=(194, 24, 91, 255), anchor="mm")
stamp = stamp.rotate(-10, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (660, 648), stamp)

img.save(OUT, "PNG")
print("OK:", OUT, img.size, len(open(OUT, "rb").read()), "bytes")
