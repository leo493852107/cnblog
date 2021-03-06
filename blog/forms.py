# !usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:leo
@time: 2021/10/31
@file: forms.py
@function:
@modify:
"""
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from blog.models import UserInfo


class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           error_messages={"required": "该字段不能为空"},
                           label="用户名",
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    pwd = forms.CharField(max_length=32,
                          label="密码",
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    re_pwd = forms.CharField(max_length=32,
                             label="确认密码",
                             widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=32,
                             label="邮箱",
                             widget=widgets.EmailInput(attrs={"class": "form-control"}))

    def clean_user(self):
        username = self.cleaned_data.get("user")
        user = UserInfo.objects.filter(username=username).first()
        if not user:
            return username
        else:
            raise ValidationError("该用户已经注册!")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("密码不一致!")
