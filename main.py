"""The World in One Image - 24 November 2026.

A newspaper front page drawn with nothing but the Python standard library.
Six stories first reported on Tuesday 24 November 2026, each with a headline,
a short deck and a small pictogram drawn from lines, circles and rectangles.
No network, no clock, no randomness: every run writes identical bytes.
"""

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (248, 244, 232)
INK = (28, 28, 30)
RED = (176, 32, 32)
BLUE = (28, 74, 138)
GOLD = (172, 128, 30)
GREY = (110, 108, 102)
TEAL = (32, 106, 126)
ORANGE = (208, 104, 26)
DARK = (64, 64, 68)
CREAM = (238, 230, 210)

# A 5x7 bitmap font written from scratch. Every glyph is seven rows of five
# bits, most significant bit on the left, one row per tuple entry.
FONT = {
    "A": (0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "B": (0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110),
    "C": (0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110),
    "D": (0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110),
    "E": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111),
    "F": (0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000),
    "G": (0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111),
    "H": (0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001),
    "I": (0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "J": (0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100),
    "K": (0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001),
    "L": (0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111),
    "M": (0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001),
    "N": (0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001),
    "O": (0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "P": (0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000),
    "Q": (0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101),
    "R": (0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001),
    "S": (0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110),
    "T": (0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100),
    "U": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110),
    "V": (0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100),
    "W": (0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001),
    "X": (0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001),
    "Y": (0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100),
    "Z": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111),
    "0": (0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110),
    "1": (0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110),
    "2": (0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111),
    "3": (0b11110, 0b00001, 0b00001, 0b01110, 0b00001, 0b00001, 0b11110),
    "4": (0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010),
    "5": (0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110),
    "6": (0b01110, 0b10000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110),
    "7": (0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000),
    "8": (0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110),
    "9": (0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001, 0b01110),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0b01100, 0b01100),
    ",": (0, 0, 0, 0, 0b01100, 0b00100, 0b01000),
    ":": (0, 0b01100, 0b01100, 0, 0b01100, 0b01100, 0),
    ";": (0, 0b01100, 0b01100, 0, 0b01100, 0b00100, 0b01000),
    "!": (0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0, 0b00100),
    "?": (0b01110, 0b10001, 0b00001, 0b00110, 0b00100, 0, 0b00100),
    "'": (0b00100, 0b00100, 0b01000, 0, 0, 0, 0),
    "-": (0, 0, 0, 0b01110, 0, 0, 0),
    "(": (0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010),
    ")": (0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000),
    "/": (0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000),
    "%": (0b11001, 0b11010, 0b00010, 0b00100, 0b01000, 0b01011, 0b10011),
    "+": (0, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0),
    "&": (0b01100, 0b10010, 0b10100, 0b01000, 0b10101, 0b10010, 0b01101),
    "$": (0b00100, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100),
    '"': (0b01010, 0b01010, 0, 0, 0, 0, 0),
    "=": (0, 0, 0b11111, 0, 0b11111, 0, 0),
}

# The picture lives in one flat RGB bytearray.
PIX = bytearray(W * H * 3)
for _i in range(W * H):
    PIX[_i * 3] = PAPER[0]
    PIX[_i * 3 + 1] = PAPER[1]
    PIX[_i * 3 + 2] = PAPER[2]


def px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        PIX[i] = color[0]
        PIX[i + 1] = color[1]
        PIX[i + 2] = color[2]


def fill_rect(x, y, w, h, color):
    for yy in range(max(0, y), min(H, y + h)):
        base = (yy * W + max(0, x)) * 3
        for xx in range(max(0, x), min(W, x + w)):
            PIX[base] = color[0]
            PIX[base + 1] = color[1]
            PIX[base + 2] = color[2]
            base += 3


def frame(x, y, w, h, color, t=2):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)


def line(x0, y0, x1, y1, color, t=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        for a in range(t):
            for b in range(t):
                px(x0 + a, y0 + b, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def disc(cx, cy, r, color, filled=True):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
            if filled:
                if d <= r * r:
                    px(xx, yy, color)
            else:
                if r * r - 2 * r <= d <= r * r:
                    px(xx, yy, color)


def char_w(scale):
    return 6 * scale


def text_w(s, scale):
    return len(s) * char_w(scale)


def draw_text(s, x, y, scale, color):
    s = s.upper()
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT["?"])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    fill_rect(cx + col * scale, y + row * scale,
                              scale, scale, color)
        cx += char_w(scale)
    return cx


def draw_centered(s, cx, y, scale, color):
    draw_text(s, cx - text_w(s, scale) // 2, y, scale, color)


def wrap(s, width, scale):
    words = s.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paragraph(s, x, y, width, scale, color, leading=None):
    if leading is None:
        leading = 9 * scale
    for ln in wrap(s, width, scale):
        draw_text(ln, x, y, scale, color)
        y += leading
    return y


# ---- pictograms, one per story -------------------------------------------

def pic_scales(cx, cy, s, color):
    # Scales of justice: pole, beam, two hanging pans.
    line(cx, cy - 46 * s // 10, cx, cy + 40 * s // 10, color, 3)
    line(cx - 44 * s // 10, cy - 30 * s // 10,
         cx + 44 * s // 10, cy - 30 * s // 10, color, 3)
    disc(cx, cy - 52 * s // 10, 5 * s // 10, color)
    for side in (-1, 1):
        px0 = cx + side * 44 * s // 10
        line(px0, cy - 30 * s // 10, px0 - 16 * s // 10,
             cy + 6 * s // 10, color, 2)
        line(px0, cy - 30 * s // 10, px0 + 16 * s // 10,
             cy + 6 * s // 10, color, 2)
        line(px0 - 16 * s // 10, cy + 6 * s // 10,
             px0 + 16 * s // 10, cy + 6 * s // 10, color, 2)
    fill_rect(cx - 30 * s // 10, cy + 40 * s // 10, 60 * s // 10, 5, color)


def pic_satellite(cx, cy, s, color):
    # A satellite: body, two solar wings, a dish.
    fill_rect(cx - 14 * s // 10, cy - 10 * s // 10, 28 * s // 10,
              20 * s // 10, color)
    fill_rect(cx - 52 * s // 10, cy - 6 * s // 10, 34 * s // 10,
              12 * s // 10, color)
    fill_rect(cx + 18 * s // 10, cy - 6 * s // 10, 34 * s // 10,
              12 * s // 10, color)
    line(cx + 14 * s // 10, cy + 10 * s // 10, cx + 30 * s // 10,
         cy + 30 * s // 10, color, 3)
    disc(cx + 34 * s // 10, cy + 34 * s // 10, 8 * s // 10, color,
         filled=False)
    for gx in range(-50, 55, 10):
        line(cx + gx * s // 10, cy - 6 * s // 10,
             cx + gx * s // 10, cy + 6 * s // 10, BLUE, 1)


def pic_drone(cx, cy, s, color):
    # A quadcopter seen from above: arms and four rotors.
    line(cx - 34 * s // 10, cy - 34 * s // 10, cx + 34 * s // 10,
         cy + 34 * s // 10, color, 3)
    line(cx - 34 * s // 10, cy + 34 * s // 10, cx + 34 * s // 10,
         cy - 34 * s // 10, color, 3)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        disc(cx + dx * 34 * s // 10, cy + dy * 34 * s // 10, 13 * s // 10,
             color, filled=False)
    disc(cx, cy, 12 * s // 10, color)
    disc(cx, cy, 5 * s // 10, PAPER)


def pic_globe(cx, cy, s, color):
    # A globe circled by a small orbit: the AI story.
    disc(cx, cy, 38 * s // 10, color, filled=False)
    for k in range(-2, 3):
        x = cx + k * 14 * s // 10
        line(x, cy - 34 * s // 10, x, cy + 34 * s // 10, color, 1)
    line(cx - 38 * s // 10, cy, cx + 38 * s // 10, cy, color, 1)
    line(cx - 38 * s // 10, cy - 34 * s // 10, cx + 38 * s // 10,
         cy + 34 * s // 10, GOLD, 2)
    disc(cx + 30 * s // 10, cy - 30 * s // 10, 6 * s // 10, RED)


def pic_mountain(cx, cy, s, color):
    # Two peaks with a crack running down the taller one.
    line(cx - 48 * s // 10, cy + 34 * s // 10, cx - 12 * s // 10,
         cy - 30 * s // 10, color, 3)
    line(cx - 12 * s // 10, cy - 30 * s // 10, cx + 8 * s // 10,
         cy + 34 * s // 10, color, 3)
    line(cx + 2 * s // 10, cy + 34 * s // 10, cx + 26 * s // 10,
         cy - 6 * s // 10, color, 3)
    line(cx + 26 * s // 10, cy - 6 * s // 10, cx + 52 * s // 10,
         cy + 34 * s // 10, color, 3)
    line(cx - 12 * s // 10, cy - 30 * s // 10, cx - 6 * s // 10,
         cy - 8 * s // 10, RED, 3)
    line(cx - 6 * s // 10, cy - 8 * s // 10, cx - 14 * s // 10,
         cy + 12 * s // 10, RED, 3)
    line(cx - 14 * s // 10, cy + 12 * s // 10, cx - 8 * s // 10,
         cy + 34 * s // 10, RED, 3)


def pic_cross(cx, cy, s, color):
    # A medical cross with three small dots: the measles story.
    fill_rect(cx - 10 * s // 10, cy - 34 * s // 10, 20 * s // 10,
              68 * s // 10, color)
    fill_rect(cx - 34 * s // 10, cy - 10 * s // 10, 68 * s // 10,
              20 * s // 10, color)
    for dx, dy in ((-44, -28), (44, -28), (0, 40)):
        disc(cx + dx * s // 10, cy + dy * s // 10, 5 * s // 10, RED)


# ---- page layout ----------------------------------------------------------

def kicker(x, y, label, color):
    draw_text(label, x, y, 2, color)


def headline_block(x, y, width, head, deck, accent, pic, pic_cx, pic_cy):
    kicker(x, y, "24 NOV 2026", GREY)
    y += 22
    y = paragraph(head, x, y, width, 3, INK)
    y += 8
    y = paragraph(deck, x, y, width, 2, DARK)
    return y


def draw_page():
    fill_rect(0, 0, W, H, PAPER)
    # Masthead.
    draw_centered("THE WORLD IN ONE IMAGE", W // 2, 30, 5, INK)
    fill_rect(24, 84, W - 48, 3, INK)
    draw_centered("TUESDAY, 24 NOVEMBER 2026  -  SIX STORIES, ONE DAY",
                  W // 2, 96, 2, GREY)
    fill_rect(24, 116, W - 48, 2, INK)

    # Lead story: the ICJ genocide ruling, top left.
    frame(24, 130, 640, 330, INK)
    pic_scales(160, 300, 10, BLUE)
    headline_block(300, 156, 340,
                   "MYANMAR GUILTY OF GENOCIDE",
                   "The world court rules Myanmar's forces committed "
                   "genocide against the Rohingya in 2017 - the first "
                   "time the court has found a state responsible. "
                   "Fourteen nations back the ruling.",
                   RED, pic_scales, 160, 300)
    draw_text("LEAD STORY", 300, 420, 2, RED)

    # Side story: NATO and the space threat, top right.
    frame(680, 130, 320, 330, INK)
    pic_satellite(840, 218, 10, TEAL)
    headline_block(700, 282, 280,
                   "NATO VOWS SPACE DEFENCE",
                   "NATO will defend space after reports of a Russian "
                   "nuclear-armed satellite within 60 days.",
                   TEAL, pic_satellite, 840, 225)

    # Middle row, left: the capture of El Chapo Isidro.
    frame(24, 476, 488, 252, INK)
    pic_drone(120, 600, 8, ORANGE)
    headline_block(220, 500, 272,
                   "US DRONE HELPS CATCH EL CHAPO ISIDRO",
                   "A US surveillance drone over Sinaloa helped "
                   "Mexican forces capture Fausto Isidro Meza Flores. "
                   "Mexico will try him at home.",
                   ORANGE, pic_drone, 120, 600)

    # Middle row, right: the UN chief on AI.
    frame(512, 476, 488, 252, INK)
    pic_globe(608, 600, 8, BLUE)
    headline_block(708, 500, 272,
                   "UN CHIEF: AI RULES WITHIN A YEAR",
                   "Antonio Guterres calls on states to build a "
                   "multilateral framework to manage AI risks before "
                   "his term ends.",
                   BLUE, pic_globe, 608, 600)

    # Bottom row, left: the Nepal earthquake.
    frame(24, 744, 488, 256, INK)
    pic_mountain(120, 868, 8, GOLD)
    headline_block(220, 768, 272,
                   "QUAKE SHAKES NEPAL BORDER",
                   "A magnitude 5.6 earthquake strikes Koshi province "
                   "in Nepal, near the border with China.",
                   GOLD, pic_mountain, 120, 868)

    # Bottom row, right: measles in Pennsylvania.
    frame(512, 744, 488, 256, INK)
    pic_cross(608, 868, 8, RED)
    headline_block(708, 768, 272,
                   "NINTH MEASLES DEATH IN PENNSYLVANIA",
                   "A ninth death is linked to the measles outbreak "
                   "spreading across 46 counties in the state.",
                   RED, pic_cross, 608, 868)

    fill_rect(24, 1012, W - 48, 2, INK)


# ---- PNG writer, hand-built from zlib and struct --------------------------

def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += PIX[y * W * 3:(y + 1) * W * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    draw_page()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    write_png(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
