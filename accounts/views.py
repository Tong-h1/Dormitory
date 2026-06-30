from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password != password2:
            messages.error(request, "两次密码不一致")
            return render(request, "registration/register.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, "用户名已存在")
            return render(request, "registration/register.html")
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, "注册成功")
        return redirect("/")
    return render(request, "registration/register.html")
