from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "assets" / "images"
OUT = ROOT / "assets" / "marketing"
OUT.mkdir(parents=True, exist_ok=True)

PAPER = "#f2eadc"
PAPER_DEEP = "#e7dbc8"
INK = "#211f1a"
INK_SOFT = "#5e594f"
VERMILION = "#c63f28"
CREAM = "#fbf7ef"
SAGE = "#747d67"

FONT_DISPLAY = "C:/Windows/Fonts/STSONG.TTF"
FONT_SANS = "C:/Windows/Fonts/Deng.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/Dengb.ttf"


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size, index=index)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS)


def draw_tracked(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    text_font: ImageFont.FreeTypeFont,
    fill: str,
    tracking: int = 0,
) -> None:
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=text_font, fill=fill)
        x += int(draw.textlength(char, font=text_font)) + tracking


def add_gradient(
    image: Image.Image,
    box: tuple[int, int, int, int],
    start: tuple[int, int, int, int],
    end: tuple[int, int, int, int],
    horizontal: bool = False,
) -> None:
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = overlay.load()
    steps = width if horizontal else height
    for i in range(steps):
        ratio = i / max(steps - 1, 1)
        color = tuple(int(start[j] * (1 - ratio) + end[j] * ratio) for j in range(4))
        if horizontal:
            for y in range(height):
                pixels[i, y] = color
        else:
            for x in range(width):
                pixels[x, i] = color
    image.paste(overlay, (x0, y0), overlay)


def make_xianyu_cover() -> Path:
    size = (1080, 1080)
    base = cover(Image.open(IMAGES / "hero-still-life.png"), size).convert("RGBA")
    add_gradient(
        base,
        (0, 0, 760, size[1]),
        (18, 16, 13, 232),
        (18, 16, 13, 0),
        horizontal=True,
    )
    add_gradient(base, (0, 730, size[0], size[1]), (18, 16, 13, 0), (18, 16, 13, 220))
    draw = ImageDraw.Draw(base)

    draw_tracked(draw, (62, 54), "见物 STUDIO", font(FONT_SANS_BOLD, 24), CREAM, 4)
    draw.text((62, 115), "AI-ASSISTED / PRODUCT VISUALS", font=font(FONT_SANS, 17), fill=(251, 247, 239, 180))
    draw.text((62, 290), "不重拍，", font=font(FONT_DISPLAY, 104), fill=CREAM)
    draw.text((62, 395), "也能上新图。", font=font(FONT_DISPLAY, 104), fill="#ef7b62")
    draw.text((65, 535), "商品主体保留 / 场景光线重做", font=font(FONT_SANS_BOLD, 28), fill=CREAM)
    draw.text((65, 585), "手机原图也能做成能上架的场景主图", font=font(FONT_SANS, 25), fill=(251, 247, 239, 210))

    draw.rounded_rectangle((62, 760, 405, 855), radius=8, fill=VERMILION)
    draw.text((86, 779), "首单体验", font=font(FONT_SANS_BOLD, 25), fill=CREAM)
    draw.text((227, 765), "¥39", font=font(FONT_DISPLAY, 58), fill=CREAM)

    draw.text((66, 916), "24H 首版", font=font(FONT_SANS_BOLD, 21), fill=(251, 247, 239, 220))
    draw.text((250, 916), "1 次关键点修改", font=font(FONT_SANS_BOLD, 21), fill=(251, 247, 239, 220))
    draw.text((530, 916), "主图尺寸适配", font=font(FONT_SANS_BOLD, 21), fill=(251, 247, 239, 220))

    draw.rectangle((0, 0, 8, 1080), fill=VERMILION)
    output = OUT / "xianyu-cover-1x1.png"
    base.convert("RGB").save(output, quality=95)
    return output


def make_xianyu_gallery() -> Path:
    size = (1080, 1080)
    canvas = Image.new("RGB", size, PAPER)
    draw = ImageDraw.Draw(canvas)
    draw.text((48, 42), "见物 STUDIO", font=font(FONT_SANS_BOLD, 22), fill=INK)
    draw.text((48, 104), "三种最常见的上新需求", font=font(FONT_DISPLAY, 54), fill=INK)
    draw.text((50, 182), "SELECTED WORKS / CONCEPT VISUALS", font=font(FONT_SANS, 15), fill=INK_SOFT)

    cards = [
        (IMAGES / "fragrance-stone.png", "香氛", "夏日场景主图"),
        (IMAGES / "hero-still-life.png", "家居", "品牌氛围图"),
        (IMAGES / "leather-tote.png", "配饰", "生活方式种草图"),
    ]
    x_positions = [48, 390, 732]
    top, width, height = 250, 300, 650
    for x, (path, label, sublabel) in zip(x_positions, cards, strict=True):
        img = cover(Image.open(path), (width, height))
        canvas.paste(img, (x, top))
        draw.rectangle((x, top, x + width, top + 4), fill=VERMILION)
        draw.text((x, top + height + 18), label, font=font(FONT_DISPLAY, 27), fill=INK)
        draw.text((x, top + height + 56), sublabel, font=font(FONT_SANS, 16), fill=INK_SOFT)

    draw.line((48, 1007, 1032, 1007), fill=(33, 31, 26, 55), width=1)
    draw.text((48, 1023), "AI 辅助生成 + 人工筛选修图", font=font(FONT_SANS, 15), fill=INK_SOFT)
    draw.text((820, 1023), "01 / 03", font=font(FONT_SANS_BOLD, 15), fill=VERMILION)
    output = OUT / "xianyu-gallery-1x1.png"
    canvas.save(output)
    return output


def make_xianyu_pricing() -> Path:
    size = (1080, 1080)
    canvas = Image.new("RGB", size, CREAM)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 14, 1080), fill=VERMILION)
    draw.text((54, 46), "见物 STUDIO", font=font(FONT_SANS_BOLD, 22), fill=INK)
    draw.text((54, 121), "价格写清楚，", font=font(FONT_DISPLAY, 76), fill=INK)
    draw.text((54, 207), "不让你猜。", font=font(FONT_DISPLAY, 76), fill=VERMILION)
    draw.text((56, 310), "先看小样，确认方向再继续。", font=font(FONT_SANS, 22), fill=INK_SOFT)

    rows = [
        ("01", "清场图", "¥19", "/ 张", "去背景 · 清杂物 · 补自然阴影"),
        ("02", "场景主图", "¥49", "/ 张", "定制场景 · 两个尺寸 · 1 次修改"),
        ("03", "上新套图", "¥129", "/ 3 张", "统一视觉 · 2 次修改 · 新品上架"),
    ]
    y = 410
    for index, title, price, unit, detail in rows:
        draw.line((56, y, 1024, y), fill=(33, 31, 26, 62), width=1)
        draw.text((56, y + 28), index, font=font(FONT_DISPLAY, 22), fill=VERMILION)
        draw.text((125, y + 24), title, font=font(FONT_DISPLAY, 39), fill=INK)
        draw.text((530, y + 17), price, font=font(FONT_DISPLAY, 54), fill=INK)
        draw.text((728, y + 42), unit, font=font(FONT_SANS, 18), fill=INK_SOFT)
        draw.text((125, y + 87), detail, font=font(FONT_SANS, 17), fill=INK_SOFT)
        y += 164

    draw.line((56, y, 1024, y), fill=(33, 31, 26, 62), width=1)
    draw.rounded_rectangle((56, 939, 1024, 1015), radius=5, fill=INK)
    draw.text((80, 958), "首发体验：首张场景主图 ¥39，每人限 1 张", font=font(FONT_SANS_BOLD, 21), fill=CREAM)
    draw.text((836, 1030), "02 / 03", font=font(FONT_SANS_BOLD, 15), fill=VERMILION)
    output = OUT / "xianyu-pricing-1x1.png"
    canvas.save(output)
    return output


def make_xianyu_process() -> Path:
    size = (1080, 1080)
    canvas = Image.new("RGB", size, INK)
    draw = ImageDraw.Draw(canvas)
    draw.text((54, 46), "见物 STUDIO", font=font(FONT_SANS_BOLD, 22), fill=CREAM)
    draw.text((54, 126), "四步，把图交出去。", font=font(FONT_DISPLAY, 70), fill=CREAM)
    draw.text((56, 221), "你负责把产品拍清楚，剩下的交给见物。", font=font(FONT_SANS, 21), fill=(251, 247, 239, 170))

    steps = [
        ("01", "发原图", "3–5 张清晰照片，\n说清平台、品类和用途。"),
        ("02", "定方向", "确认场景与色调，\n支付 50% 定金。"),
        ("03", "看首版", "24 小时内看小样，\n确认主体和光线。"),
        ("04", "改完交付", "关键点修改，\n结清后交高清文件。"),
    ]
    x_positions = [54, 562]
    y_positions = [355, 675]
    for i, (number, title, body) in enumerate(steps):
        x = x_positions[i % 2]
        y = y_positions[i // 2]
        draw.rectangle((x, y, x + 464, y + 242), outline=(251, 247, 239, 50), width=1)
        draw.text((x + 24, y + 22), number, font=font(FONT_DISPLAY, 21), fill="#e27d66")
        draw.text((x + 24, y + 63), title, font=font(FONT_DISPLAY, 38), fill=CREAM)
        draw.multiline_text(
            (x + 24, y + 128),
            body,
            font=font(FONT_SANS, 20),
            fill=(251, 247, 239, 178),
            spacing=11,
        )

    draw.text((54, 1014), "标准 24 小时首版 · 加急 12 小时 +¥30", font=font(FONT_SANS, 16), fill=(251, 247, 239, 150))
    draw.text((837, 1014), "03 / 03", font=font(FONT_SANS_BOLD, 15), fill="#e27d66")
    output = OUT / "xianyu-process-1x1.png"
    canvas.save(output)
    return output


def make_xiaohongshu_cover() -> Path:
    size = (1080, 1440)
    base = cover(Image.open(IMAGES / "fragrance-stone.png"), size).convert("RGBA")
    add_gradient(base, (0, 0, 1080, 620), (22, 20, 16, 175), (22, 20, 16, 0))
    add_gradient(base, (0, 850, 1080, 1440), (22, 20, 16, 0), (22, 20, 16, 230))
    draw = ImageDraw.Draw(base)

    draw_tracked(draw, (58, 54), "见物 STUDIO", font(FONT_SANS_BOLD, 23), CREAM, 4)
    draw.text((59, 106), "AI-ASSISTED PRODUCT VISUALS", font=font(FONT_SANS, 16), fill=(251, 247, 239, 190))
    draw.text((58, 192), "别再为一张商品图", font=font(FONT_DISPLAY, 68), fill=CREAM)
    draw.text((58, 278), "重拍一整批货", font=font(FONT_DISPLAY, 68), fill="#f08a71")
    draw.text((60, 385), "手机原图，也能改成有购买欲的场景主图。", font=font(FONT_SANS, 24), fill=CREAM)

    draw.rectangle((58, 1010, 1022, 1012), fill=(251, 247, 239, 100))
    draw.text((58, 1050), "不换产品，只重做场景、光线和氛围。", font=font(FONT_DISPLAY, 36), fill=CREAM)
    draw.text((58, 1110), "首单体验 ¥39 起 · 24 小时首版", font=font(FONT_SANS_BOLD, 22), fill=(251, 247, 239, 210))
    draw.text((58, 1320), "见物 STUDIO / JIANWU VISUAL", font=font(FONT_SANS, 15), fill=(251, 247, 239, 160))

    output = OUT / "xiaohongshu-cover-3x4.png"
    base.convert("RGB").save(output, quality=95)
    return output


def main() -> None:
    outputs = [
        make_xianyu_cover(),
        make_xianyu_gallery(),
        make_xianyu_pricing(),
        make_xianyu_process(),
        make_xiaohongshu_cover(),
    ]
    for output in outputs:
        with Image.open(output) as image:
            print(f"{output}\t{image.width}x{image.height}\t{output.stat().st_size} bytes")


if __name__ == "__main__":
    main()
