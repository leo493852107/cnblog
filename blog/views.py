from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from blog.forms import UserForm
from blog.models import UserInfo
from blog.utils.valid_code import get_valid_code_img


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
    data = get_valid_code_img(request)
    return HttpResponse(data)


def index(request):
    return render(request, "index.html")


def register(request):
    if request.is_ajax():
        form = UserForm(request.POST)
        response = {"user": None, "msg": None}
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")
            user = form.cleaned_data.get("user")
            password = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")
            extra_fields = {}
            if avatar_obj:
                extra_fields["avatar"] = avatar_obj
            user_obj = UserInfo.objects.create_user(username=user, password=password, email=email, **extra_fields)
        else:
            print(form.cleaned_data)
            print(form.errors)
            response["msg"] = form.errors
        return JsonResponse(response)

    form = UserForm()
    return render(request, "register.html", {"form": form})
