# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

W, H = 1920, 1080
BG = "#FFFFFF"
BLACK = "#000000"
GRAY2 = "#333333"
GRAY4 = "#666666"

FONT_DIR = "C:/Windows/Fonts"
BOLD_FONT = os.path.join(FONT_DIR, "msyhbd.ttc")
REG_FONT = os.path.join(FONT_DIR, "msyh.ttc")

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(OUT_DIR, "logo.png")
LOGO_SIZE = 64
CAR_PHOTO = os.path.join(OUT_DIR, "car_photo.png")
CHART_PHOTO = os.path.join(OUT_DIR, "chart_photo.png")


def font(bold=False, size=40):
    path = BOLD_FONT if bold else REG_FONT
    return ImageFont.truetype(path, size)


def load_logo():
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
    return logo


def paste_logo(img):
    logo = load_logo()
    margin = 40
    x = W - LOGO_SIZE - margin
    y = margin
    img.paste(logo, (x, y), logo)


def dark_chart_to_light(img):
    """Convert a dark-background chart to white-background.
    Full inversion for clean text, then restore colored pixels from original."""
    from PIL import ImageOps
    inverted = ImageOps.invert(img.convert("RGB"))
    orig_arr = np.array(img).astype(np.float32)
    inv_arr = np.array(inverted).astype(np.float32)

    r, g, b = orig_arr[:, :, 0], orig_arr[:, :, 1], orig_arr[:, :, 2]
    max_c = np.maximum(r, np.maximum(g, b))
    min_c = np.minimum(r, np.minimum(g, b))
    sat = np.where(max_c > 10, (max_c - min_c) / max_c, 0)

    colored = sat > 0.3
    blend = colored[:, :, None].astype(np.float32)
    result = blend * orig_arr + (1 - blend) * inv_arr

    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))


def new_img():
    return Image.new("RGB", (W, H), BG)


def text_w(draw, text, f):
    bbox = draw.textbbox((0, 0), text, font=f)
    return bbox[2] - bbox[0]


def text_h(draw, text, f):
    bbox = draw.textbbox((0, 0), text, font=f)
    return bbox[3] - bbox[1]


def draw_centered(draw, y, text, f, fill=BLACK):
    tw = text_w(draw, text, f)
    draw.text(((W - tw) / 2, y), text, font=f, fill=fill)


def draw_left(draw, x, y, text, f, fill=BLACK):
    draw.text((x, y), text, font=f, fill=fill)


# ─────────────────────────── 1. 封面页 ───────────────────────────
def slide_cover():
    img = new_img()
    d = ImageDraw.Draw(img)

    title = "小米SU7：C级高性能生态科技轿车"
    subtitle = "小米汽车首款力作｜极致性能·生态科技·商务旗舰"
    reporter = "汇报人：胡兆岩"
    date = "2026年03月03日"

    f_title = font(bold=True, size=72)
    f_sub = font(bold=False, size=36)
    f_info = font(bold=False, size=30)

    draw_centered(d, 300, title, f_title, BLACK)
    draw_centered(d, 420, subtitle, f_sub, GRAY2)

    draw_centered(d, 650, reporter, f_info, GRAY4)
    draw_centered(d, 710, date, f_info, GRAY4)

    paste_logo(img)
    img.save(os.path.join(OUT_DIR, "01_封面页.png"))


# ─────────────────────────── 2. 目录页 ───────────────────────────
def slide_toc():
    img = new_img()
    d = ImageDraw.Draw(img)

    f_title = font(bold=True, size=64)
    f_sub = font(bold=False, size=30)
    f_item = font(bold=False, size=34)
    f_chap = font(bold=False, size=24)

    draw_centered(d, 100, "目录", f_title, BLACK)
    draw_centered(d, 185, "CONTENTS", f_sub, GRAY4)

    items = [
        ("01", "性能标杆与高效补能", "Chapter 01"),
        ("02", "智能生态与驾驶辅助", "Chapter 02"),
        ("03", "设计美学与安全架构", "Chapter 03"),
        ("04", "市场格局与未来展望", "Chapter 04"),
    ]

    y_start = 340
    gap = 140
    for i, (num, name, chap) in enumerate(items):
        y = y_start + i * gap
        line_text = f"{num}  {name}"
        draw_left(d, 400, y, line_text, f_item, BLACK)
        draw_left(d, 400, y + 48, chap, f_chap, GRAY4)

    paste_logo(img)
    img.save(os.path.join(OUT_DIR, "02_目录页.png"))


# ─────────────────────────── 3. 章节页 ───────────────────────────
def slide_chapter():
    img = new_img()
    d = ImageDraw.Draw(img)

    f_title = font(bold=True, size=72)

    draw_centered(d, 460, "01  性能标杆与高效补能", f_title, BLACK)

    paste_logo(img)
    img.save(os.path.join(OUT_DIR, "03_章节页_01.png"))


# ─────────────────────────── 4. 正文:800V快充 ─────────────────────
def slide_800v():
    img = new_img()
    d = ImageDraw.Draw(img)

    f_title = font(bold=True, size=52)
    f_sub = font(bold=False, size=26)
    f_val = font(bold=True, size=56)
    f_label = font(bold=False, size=24)
    f_desc = font(bold=False, size=20)

    draw_centered(d, 60, "800V高压快充技术", f_title, BLACK)
    draw_centered(d, 135, '从\u201c能用\u201d到\u201c好用\u201d的跨越式体验升级，全场景高效补能解决方案', f_sub, GRAY2)

    cards = [
        ("210 kW", "峰值充电功率", "国网超充桩实测数据"),
        ("510 km", "15分钟补能续航", "Max版高效补能表现"),
        ("23 min", "10%-80% 充电耗时", "含电池预热功能优化"),
    ]

    card_w = 460
    gap = 60
    total = card_w * 3 + gap * 2
    x_start = (W - total) / 2
    y_top = 230

    for i, (val, label, desc) in enumerate(cards):
        cx = x_start + i * (card_w + gap)
        d.rectangle([cx, y_top, cx + card_w, y_top + 320], outline="#CCCCCC", width=2)

        vw = text_w(d, val, f_val)
        d.text((cx + (card_w - vw) / 2, y_top + 50), val, font=f_val, fill=BLACK)

        lw = text_w(d, label, f_label)
        d.text((cx + (card_w - lw) / 2, y_top + 150), label, font=f_label, fill=GRAY2)

        dw = text_w(d, desc, f_desc)
        d.text((cx + (card_w - dw) / 2, y_top + 210), desc, font=f_desc, fill=GRAY4)

    car = Image.open(CAR_PHOTO).convert("RGB")
    avail_w = 1840
    avail_h = H - (y_top + 320 + 30) - 20
    scale = min(avail_w / car.width, avail_h / car.height)
    new_w = int(car.width * scale)
    new_h = int(car.height * scale)
    car_resized = car.resize((new_w, new_h), Image.LANCZOS)
    paste_x = (W - new_w) // 2
    paste_y = y_top + 320 + 30 + (avail_h - new_h) // 2
    img.paste(car_resized, (paste_x, paste_y))

    paste_logo(img)
    img.save(os.path.join(OUT_DIR, "04_正文_800V快充.png"))


# ─────────────────────────── 5. 正文:极致性能 ─────────────────────
def slide_performance():
    img = new_img()
    d = ImageDraw.Draw(img)

    f_title = font(bold=True, size=44)
    f_sub = font(bold=False, size=22)
    f_section = font(bold=True, size=26)
    f_body = font(bold=False, size=20)
    f_insight_title = font(bold=True, size=20)
    f_insight = font(bold=False, size=18)

    draw_centered(d, 30, "极致性能：动力与加速", f_title, BLACK)
    draw_centered(d, 90, "SU7全系动力参数解析与HyperEngine 电机技术", f_sub, GRAY2)

    # ── 左列: 全系动力参数 ──
    lx = 80
    ly = 170
    draw_left(d, lx, ly, "▎全系动力参数 — 从日常出行到赛道竞技", f_section, BLACK)
    ly += 50
    lines_power = [
        "• 标准版：299马力，0-100km/h加速5.28秒，满足日常高效出行。",
        "• Max版：673马力，加速仅2.78秒，最高时速265km/h，媲美超跑。",
        "• Ultra版：巅峰性能1548马力，加速1.98秒，挑战物理极限。",
    ]
    for line in lines_power:
        draw_left(d, lx + 20, ly, line, f_body, GRAY2)
        ly += 36

    # ── 左列: HyperEngine ──
    ly += 30
    draw_left(d, lx, ly, "▎HyperEngine 自研电机 — 突破行业转速天花板", f_section, BLACK)
    ly += 50
    lines_motor = [
        "• 超高转速：V6/V6s电机最高转速达21,000rpm，行业领先水平。",
        "• 极致效率：采用双向全油冷散热技术，散热效率显著提升。",
        "• 技术闭环：完全自研自产，掌握核心三电技术，保障持续迭代。",
    ]
    for line in lines_motor:
        draw_left(d, lx + 20, ly, line, f_body, GRAY2)
        ly += 36

    # ── 右列: 马力对比柱状图（使用实际图片） ──
    rx = 980
    ry = 150
    draw_left(d, rx, ry, "▎各版本最大马力对比（PS）", f_section, BLACK)
    ry += 46

    chart = Image.open(CHART_PHOTO).convert("RGB")
    chart = dark_chart_to_light(chart)
    chart_avail_w = W - rx - 40
    chart_avail_h = 480
    scale_w = chart_avail_w / chart.width
    scale_h = chart_avail_h / chart.height
    scale = min(scale_w, scale_h)
    cw = int(chart.width * scale)
    ch = int(chart.height * scale)
    chart_resized = chart.resize((cw, ch), Image.LANCZOS)
    img.paste(chart_resized, (rx, ry))
    ry += ch + 20

    # ── 核心洞察 ──
    draw_left(d, rx, ry, "核心洞察", f_insight_title, BLACK)
    ry += 32

    insight = (
        "小米SU7通过阶梯式的动力配置覆盖了从家用舒适到极致赛道的"
        "全场景需求。特别是Ultra版接近1550匹的马力与1.98秒的零百加速，"
        "配合21,000rpm的高转电机，标志着小米在高性能纯电领域的硬核技术实力。"
    )
    max_chars = 40
    words = insight
    while words:
        chunk = words[:max_chars]
        words = words[max_chars:]
        draw_left(d, rx, ry, chunk, f_insight, GRAY2)
        ry += 28

    paste_logo(img)
    img.save(os.path.join(OUT_DIR, "05_正文_极致性能.png"))


# ─────────────────────────── 6. 结束页 ───────────────────────────
def slide_end():
    img = new_img()
    d = ImageDraw.Draw(img)

    f_title = font(bold=True, size=80)
    f_sub = font(bold=False, size=36)

    draw_centered(d, 380, "谢谢观看", f_title, BLACK)
    draw_centered(d, 520, "汇报人：胡兆岩", f_sub, GRAY4)

    paste_logo(img)
    img.save(os.path.join(OUT_DIR, "06_结束页.png"))


# ─────────────────────────── main ─────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    slide_cover()
    slide_toc()
    slide_chapter()
    slide_800v()
    slide_performance()
    slide_end()
    print("Done – 6 images generated.")
