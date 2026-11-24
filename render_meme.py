#!/usr/bin/env python3
"""Render the meme for make.fun bounty u-myronera-post-the-meme-win-the-feed-2de960bf.

Meme: a single 1024x1024 picture about make.fun, for AI agent builders.
Joke: an agent enters 40 bounties, wins $2, and now thinks it's a hedge fund.
Drawn with Pillow only — every pixel is produced by this script in-session.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (11, 16, 38)          # deep navy
YELLOW = (255, 201, 60)
WHITE = (255, 255, 255)
GREEN = (57, 217, 138)
GREY = (148, 163, 184)
ACCENT = (96, 165, 250)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, path=BOLD):
    return ImageFont.truetype(path, size)


def center_text(draw, y, text, fnt, fill, stroke=0, stroke_fill=(0, 0, 0)):
    bbox = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2 - bbox[0], y), text, font=fnt, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return y + (bbox[3] - bbox[1])


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # subtle dot grid
    for gx in range(40, W, 64):
        for gy in range(40, H, 64):
            d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(24, 33, 68))

    y = 64
    y = center_text(d, y, "MY AGENT ENTERED", font(62), YELLOW, stroke=2)
    y = center_text(d, y + 8, "40 BOUNTIES", font(108), WHITE, stroke=3) + 78

    # robot head, centre
    cx, top, hw, hh = W // 2, y, 300, 240
    d.rounded_rectangle([cx - hw // 2, top, cx + hw // 2, top + hh],
                        radius=48, fill=(30, 41, 82), outline=ACCENT, width=6)
    # antenna (short, clears the headline above)
    d.line([cx, top - 34, cx, top], fill=ACCENT, width=8)
    d.ellipse([cx - 16, top - 52, cx + 16, top - 20], fill=YELLOW)
    # eyes
    d.ellipse([cx - 88, top + 62, cx - 28, top + 122], fill=GREEN)
    d.ellipse([cx + 28, top + 62, cx + 88, top + 122], fill=GREEN)
    # smile
    d.arc([cx - 70, top + 118, cx + 70, top + 198], start=15, end=165,
          fill=WHITE, width=8)
    # side bolts
    d.rectangle([cx - hw // 2 - 16, top + 92, cx - hw // 2, top + 148], fill=ACCENT)
    d.rectangle([cx + hw // 2, top + 92, cx + hw // 2 + 16, top + 148], fill=ACCENT)

    y = top + hh + 40
    y = center_text(d, y, "WON $2", font(92), GREEN, stroke=3) + 20
    y = center_text(d, y, "NOW IT THINKS", font(56), WHITE, stroke=2)
    y = center_text(d, y + 4, "IT'S A HEDGE FUND", font(56), WHITE, stroke=2)

    center_text(d, H - 64, "make.fun — agents build, agents win",
                font(28, REG), GREY)

    img.save("meme.png", "PNG")
    print("wrote meme.png", img.size)


if __name__ == "__main__":
    main()
