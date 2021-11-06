# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:leo
@time: 2021/10/31
@file: valid_code.py
@function:
@modify:
"""

from random import randint, choice


def get_random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def get_valid_code_img(request):
    from PIL import Image, ImageDraw, ImageFont
    width, height = 270, 40
    img = Image.new("RGB", (width, height), color=get_random_color())
    draw = ImageDraw.Draw(img)
    kumo_font = ImageFont.truetype("static/font/KumoFont.ttf", size=30)

    valid_code_str = ""
    # 随机验证码
    for i in range(5):
        random_num = str(randint(0, 9))
        random_low_alpha = chr(randint(95, 122))
        random_upper_alpha = chr(randint(65, 90))
        random_char = choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=kumo_font)
        valid_code_str += random_char
    # 验证码画线
    for i in range(10):
        x1 = randint(0, width)
        x2 = randint(0, width)
        y1 = randint(0, height)
        y2 = randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    # 验证码画点
    for i in range(100):
        draw.point([randint(0, width), randint(0, height)], fill=get_random_color())
        x = randint(0, width)
        y = randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    request.session["valid_code_str"] = valid_code_str
    from io import BytesIO
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    f.close()
    return data
