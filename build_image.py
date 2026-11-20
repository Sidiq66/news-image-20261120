# build_image.py — draws entry.png for the news-image-20261120 entry.
#
# One image that sums up the world news of Friday 20 November 2026,
# drawn as a newspaper front page. Every fact in the picture was checked
# against at least two news sources on the morning of 20 Nov 2026
# (see NEWS_BRIEF_20NOV.md in the makefun workspace). No photographs,
# no downloaded assets: the page is drawn with PIL shapes and the
# machine's own Liberation/DejaVu fonts, at 2x size and downscaled,
# so the text stays crisp. Output: entry.png, 1024x1024, beside this
# file.
import math
import os

from PIL import Image, ImageDraw, ImageFont

K = 2  # supersampling factor
W = H = 1024

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANSI = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, int(size * K))


def X(v):
    return int(v * K)


PAPER = (245, 239, 226)
PANEL = (255, 253, 246)
INK = (24, 25, 30)
GRAY = (110, 104, 92)
RED = (158, 27, 27)
TEAL = (11, 110, 153)
BLUE = (30, 79, 156)
GREEN = (20, 102, 58)
ORANGE = (179, 92, 18)
GOLD = (232, 179, 60)

img = Image.new("RGB", (W * K, H * K), PAPER)
d = ImageDraw.Draw(img)


def rect(x0, y0, x1, y1, **kw):
    d.rectangle([X(x0), X(y0), X(x1), X(y1)], **kw)


def line(points, fill=INK, width=2):
    d.line([(X(x), X(y)) for x, y in points], fill=fill, width=X(width))


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((X(x), X(y)), s, font=font, fill=fill, anchor=anchor)


def tracked(x, y, s, font, fill, tracking=3):
    """Draw letter-spaced text; returns the x just past its end."""
    cx = x
    for ch in s:
        d.text((X(cx), X(y)), ch, font=font, fill=fill, anchor="la")
        cx += (d.textlength(ch, font=font) / K) + tracking
    return cx - tracking


def tw(s, font):
    return d.textlength(s, font=font) / K


def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, font) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def panel(x0, y0, x1, y1, accent):
    rect(x0, y0, x1, y1, fill=PANEL, outline=INK, width=3)
    rect(x0, y0, x0 + 11, y1, fill=accent)


def source_tag(x1, y1, s):
    f = F(SANSI, 13)
    text(x1 - tw(s, f) - 10, y1 - 22, s, f, fill=GRAY)


def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon([(X(x), X(y)) for x, y in pts], fill=fill)


# ---------------------------------------------------------------- masthead
line([(24, 24), (1000, 24)], width=3)
line([(24, 30), (1000, 30)], width=1)
f_title = F(SERIF, 55)
text(512, 40, "THE WORLD IN ONE IMAGE", f_title, anchor="ma")
rect(24, 108, 1000, 156, fill=INK)
f_date = F(SANSB, 29)
text(512, 117, "FRIDAY · 20 NOVEMBER 2026", f_date, fill=(255, 255, 255), anchor="ma")
line([(24, 164), (1000, 164)], width=1)

# ---------------------------------------------------------------- lead: Iran
LX0, LY0, LX1, LY1 = 24, 176, 1000, 444
panel(LX0, LY0, LX1, LY1, RED)
f_kick = F(SANSB, 20)
tracked(54, 194, "IRAN WAR · WASHINGTON", f_kick, RED, 2)
f_head = F(SERIF, 47)
text(52, 226, "TRUMP HOLDS OFF IRAN", f_head)
text(52, 282, "STRIKES UNTIL 2027", f_head)
f_cap = F(SANS, 22)
cap = ("“I am not rushing into any decision,” Trump says — new Iran "
       "strikes are put off to 2027. Israel presses for a bombing "
       "campaign; the US war bill tops $48bn.")
for i, ln in enumerate(wrap(cap, f_cap, 716)):
    text(52, 348 + i * 28, ln, f_cap)
source_tag(LX1, LY1, "Sources: Reuters · Axios · NY Post")

# calendar drawing: the decision waits for January 2027
d.rounded_rectangle([X(812), X(206), X(962), X(396)], radius=X(10),
                    fill=(255, 255, 255), outline=INK, width=X(3))
rect(812, 206, 962, 252, fill=RED)
f_cal = F(SANSB, 21)
text(887, 217, "JANUARY", f_cal, fill=(255, 255, 255), anchor="ma")
f_yr = F(SERIF, 62)
text(887, 262, "2027", f_yr, anchor="ma")
for i, dx in enumerate((-52, 0, 52)):
    d.ellipse([X(887 + dx - 7), X(352), X(887 + dx + 7), X(366)], fill=GRAY)
# pause badge over the calendar's top-right corner
d.ellipse([X(936), X(182), X(988), X(234)], fill=INK)
rect(954, 196, 962, 220, fill=(255, 255, 255))
rect(968, 196, 976, 220, fill=(255, 255, 255))

# ------------------------------------------------------- row 2: cyclone / Europe
RY0, RY1 = 460, 724
f_kick2 = F(SANSB, 18)
f_head2 = F(SERIF, 30)
f_cap2 = F(SANS, 20)

# Cyclone Akvan (left)
panel(24, RY0, 500, RY1, TEAL)
tracked(52, RY0 + 18, "CYCLONE AKVAN · INDIA", f_kick2, TEAL, 2)
for i, ln in enumerate(["NEARLY 300,000", "EVACUATED AS STORM", "NEARS LANDFALL"]):
    text(52, RY0 + 48 + i * 37, ln, f_head2)
cap = ("Landfall near Gopalpur around noon today, winds gusting "
       "to 110 km/h. 423 rescue teams deployed; 69 trains cancelled.")
for i, ln in enumerate(wrap(cap, f_cap2, 424)):
    text(52, RY0 + 168 + i * 25, ln, f_cap2)
source_tag(500, RY1, "Sources: IMD · PTI · ANI")
# spiral icon: storm swirl with an eye
cx, cy = 442, RY0 + 66
for r, a0 in [(31, 300), (22, 130), (13, 210)]:
    d.arc([X(cx - r), X(cy - r), X(cx + r), X(cy + r)],
          start=a0, end=a0 + 300, fill=TEAL, width=X(6))
d.ellipse([X(cx - 4), X(cy - 4), X(cx + 4), X(cy + 4)], fill=TEAL)

# Europe / Ukraine talks (right)
panel(524, RY0, 1000, RY1, BLUE)
tracked(552, RY0 + 18, "UKRAINE WAR · BERLIN", f_kick2, BLUE, 2)
for i, ln in enumerate(["EUROPE READY FOR", "TALKS WITH RUSSIA", "TO END THE WAR"]):
    text(552, RY0 + 48 + i * 37, ln, f_head2)
cap = ("Hours after the Shenzhen summit, Ukraine’s allies agree a "
       "united position in Berlin. Merz: Moscow’s demands are "
       "“not realistic”.")
for i, ln in enumerate(wrap(cap, f_cap2, 424)):
    text(552, RY0 + 168 + i * 25, ln, f_cap2)
source_tag(1000, RY1, "Source: BBC News")
# circle of stars icon
cx, cy = 930, RY0 + 66
d.ellipse([X(cx - 32), X(cy - 32), X(cx + 32), X(cy + 32)], fill=BLUE)
for i in range(12):
    ang = i * math.pi / 6
    star(cx + 21 * math.cos(ang), cy + 21 * math.sin(ang), 5.5, GOLD)

# ------------------------------------------------------- row 3: markets / COP31
SY0, SY1 = 738, 938
f_head3 = F(SERIF, 28)
f_cap3 = F(SANS, 19)

# Anthropic IPO + Wall Street (left)
panel(24, SY0, 500, SY1, GREEN)
tracked(52, SY0 + 16, "MARKETS · NEW YORK", f_kick2, GREEN, 2)
text(52, SY0 + 46, "BIGGEST IPO EVER,", f_head3)
text(52, SY0 + 80, "WALL ST STILL SLIDES", f_head3)
cap = ("Anthropic raises $81bn in a record debut, closing at $97 — "
       "valued near $1.5tn. Yet the S&P 500 falls 2% to a "
       "seven-month low.")
for i, ln in enumerate(wrap(cap, f_cap3, 424)):
    text(52, SY0 + 122 + i * 24, ln, f_cap3)
source_tag(500, SY1, "Source: Reuters")
# bars up, arrow down icon
bx, by = 396, SY0 + 66
for i, bh in enumerate((16, 26, 38)):
    rect(bx + i * 26, by + 44 - bh, bx + i * 26 + 18, by + 44, fill=GREEN)
line([(bx - 4, by + 50), (bx + 84, by + 50)], width=2)
pts = [(bx + 2, by + 6), (bx + 44, by + 20), (bx + 80, by + 40)]
line(pts, fill=RED, width=4)
d.polygon([(X(bx + 80), X(by + 40)), (X(bx + 66), X(by + 38)),
           (X(bx + 76), X(by + 27))], fill=RED)

# COP31 closing day (right)
panel(524, SY0, 1000, SY1, ORANGE)
tracked(552, SY0 + 16, "CLIMATE SUMMIT · ANTALYA", f_kick2, ORANGE, 2)
text(552, SY0 + 46, "COP31 GOES TO", f_head3)
text(552, SY0 + 80, "THE WIRE", f_head3)
cap = ("A slimmed-down draft deal drops every mention of fossil "
       "fuels, and nearly 200 countries still hunt consensus "
       "at the close.")
for i, ln in enumerate(wrap(cap, f_cap3, 424)):
    text(552, SY0 + 122 + i * 24, ln, f_cap3)
source_tag(1000, SY1, "Sources: Reuters · Asiatoday")
# globe icon
cx, cy = 934, SY0 + 62
d.ellipse([X(cx - 30), X(cy - 30), X(cx + 30), X(cy + 30)], outline=ORANGE, width=X(3))
d.ellipse([X(cx - 13), X(cy - 30), X(cx + 13), X(cy + 30)], outline=ORANGE, width=X(2))
line([(cx - 30, cy), (cx + 30, cy)], fill=ORANGE, width=2)
line([(cx - 26, cy - 16), (cx + 26, cy - 16)], fill=ORANGE, width=2)
line([(cx - 26, cy + 16), (cx + 26, cy + 16)], fill=ORANGE, width=2)

# ---------------------------------------------------------------- ticker
rect(24, 952, 1000, 1008, fill=INK)
f_tick = F(SANS, 17)
f_tickb = F(SANSB, 17)
x_end = tracked(44, 961, "ALSO TODAY", f_tickb, GOLD, 2)
text(x_end + 18, 961,
     "Trump posthumously pardons baseball legend Pete Rose, who died in 2024",
     f_tick, fill=(255, 255, 255))
text(44, 984,
     "GTA VI’s launch-day sales estimated at $1.84bn — about 19 million copies (Sensor Tower)",
     f_tick, fill=(255, 255, 255))

img = img.resize((W, H), Image.LANCZOS)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
