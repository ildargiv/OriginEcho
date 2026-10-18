# -*- coding: utf-8 -*-
"""Генерирует иконку OriginEcho (icon.ico): тёмный скруглённый квадрат,
бронзовая рамка и монограмма OE. Запуск: python build/make_icon.py"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "icon.ico")

BG, ACCENT, INK = (16, 19, 24), (226, 179, 92), (234, 238, 243)
SIZES = [16, 24, 32, 48, 64, 128, 256]
FONT_CANDIDATES = [r"C:\Windows\Fonts\seguibd.ttf", r"C:\Windows\Fonts\segoeuib.ttf",
                   r"C:\Windows\Fonts\arialbd.ttf"]


def _font(px):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return ImageFont.truetype(p, px)
    return ImageFont.load_default()


def render(px):
    s = px * 4  # рисуем с запасом, потом уменьшаем
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pad = s // 12
    d.rounded_rectangle([pad, pad, s - pad, s - pad], radius=s // 5,
                        fill=BG + (255,))
    d.rounded_rectangle([pad, pad, s - pad, s - pad], radius=s // 5,
                        outline=ACCENT + (255,), width=max(2, s // 40))
    f = _font(int(s * 0.46))
    tw, th = d.textbbox((0, 0), "OE", font=f)[2:]
    d.text(((s - tw) / 2, (s - th) / 2 - s // 40), "OE", font=f, fill=INK + (255,))
    return im.resize((px, px), Image.LANCZOS)


images = [render(px) for px in SIZES]
images[-1].save(OUT, format="ICO", sizes=[(px, px) for px in SIZES],
                append_images=images[:-1])
print("OK:", OUT, os.path.getsize(OUT), "bytes")
