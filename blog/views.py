from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.

def login(request):
    if request.method == "POST":
        response = {"user": None, "msg": None}
        username = request.POST.get("username")
        password = request.POST.get("password")
        valid_code = request.POST.get("valid_code")
        if valid_code.upper() == request.session.get("valid_code_str").upper():
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user=user)
                response["user"] = user.username
            else:
                response["msg"] = "用户名或密码错误"
        else:
            response["msg"] = "验证码错误"
        return JsonResponse(response)

    return render(request, "login.html")


def get_valid_code_image(request):
    from random import randint, choice

    def get_random_color():
        return randint(0, 255), randint(0, 255), randint(0, 255)

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

    print(valid_code_str)
    request.session["valid_code_str"] = valid_code_str
    from io import BytesIO
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    f.close()

    return HttpResponse(data)


def index(request):
    return render(request, "index.html")
