# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import os

W, H = 150, 154
BG_FILL = (250, 245, 255)
PURPLE = (177, 78, 255)
WHITE = (255, 255, 255)
LINE_W = 5

OUT = os.path.dirname(os.path.abspath(__file__))

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

d.rounded_rectangle([4, 4, W - 5, H - 5], radius=28, fill=BG_FILL)

pad = 32
fx1, fy1 = pad, pad + 6
fx2, fy2 = W - pad, H - pad - 4
d.rounded_rectangle([fx1, fy1, fx2, fy2], radius=8, outline=PURPLE, width=LINE_W)

sun_cx, sun_cy, sun_r = fx1 + 26, fy1 + 22, 10
d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
          fill=PURPLE)

mid_x = (fx1 + fx2) / 2
peak1_x = fx1 + (fx2 - fx1) * 0.35
peak1_y = fy1 + (fy2 - fy1) * 0.38
base_y = fy2

mountain1 = [
    (fx1, base_y),
    (peak1_x, peak1_y),
    (mid_x + 4, base_y),
]
d.polygon(mountain1, fill=PURPLE)

peak2_x = fx1 + (fx2 - fx1) * 0.70
peak2_y = fy1 + (fy2 - fy1) * 0.28
mountain2 = [
    (mid_x - 8, base_y),
    (peak2_x, peak2_y),
    (fx2, base_y),
]
d.polygon(mountain2, fill=PURPLE)

img.save(os.path.join(OUT, "icon_background_image.png"))
print("Done")
