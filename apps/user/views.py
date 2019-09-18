from django.contrib import auth
from .models import Ouser
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UserForm, loginForm, ProfileForm
import re


@csrf_exempt  # 注册
def register_view(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        next_to = request.POST.get('next', 0)
        if form.is_valid():  # 判断表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            context = {'username': username, 'pwd': password, 'email': email}
            if password.isdigit():
                context['pwd_error'] = 'nums'
                return render(request, 'account/signup.html', context)
            if password != password2:
                context['pwd_error'] = 'unequal'
                return render(request, 'account/signup.html', context)

            # 判断用户是否存在
            user = Ouser.objects.filter(username=username)
            Email = Ouser.objects.filter(email=email)
            pwd_length = len(password)
            # 校验用户填写的信息
            if pwd_length < 8 or pwd_length > 20:
                context['pwd_error'] = 'length'
                return render(request, 'account/signup.html', context)
            user_length = len(username)
            if user_length < 5 or user_length > 20:
                context['user_error'] = 'length'
                return render(request, 'account/signup.html', context)
            if user:
                context['user_error'] = 'exit'
                return render(request, 'account/signup.html', context)
            if not re.match('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', email):
                context['email_error'] = 'format'
                return render(request, 'account/signup.html', context)
            if Email:
                context['email_error'] = 'exit'
                return render(request, 'account/signup.html', context)

            # 添加数据库(还可以加一些字段的处理)
            user = Ouser.objects.create_user(username=username, password=password, email=email)
            user.save()
            user = auth.authenticate(username=username, password=password)

            # 添加到session
            request.session['username'] = username
            request.session['uid'] = user.id
            request.session['nick'] = ''

            # 调用auth登录
            auth.login(request, user)
            # 重定向到首页
            if next_to == '':
                next_to = '/'
            return redirect(next_to)
        else:
            next_to = request.POST.get('next', '/')
            context = {'isLogin': False}
            context['next_to'] = next_to
        # 将req， 页面，以及context{}(要传入html文件中的内容包含在字典里)返回
        return render(request, 'account/signup.html', context)


@csrf_exempt  # 登录
def login_view(request):
    context = {}
    if request.method == "POST":
        form = loginForm(request.POST)
        next_to = request.POST.get('next', '')
        remember = request.POST.get('remember', 0)
        if form.is_valid():
            # 获取表单用户密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            context = {'username': username, 'pwd': password}
            user = authenticate(username=username, password=password)
            if next_to == '':
                next_to = '/'
            if user:
                if user.is_active:
                    # 比较成功，跳转到index
                    auth.login(request, user)
                    request.session['username'] = username
                    request.session['uid'] = user.id
                    request.session['nick'] = None
                    request.session['tid'] = None
                    reqs = HttpResponseRedirect(next_to)
                    if remember != 0:
                        reqs.set_cookie('username', username)
                    else:
                        reqs.set_cookie('username', '', max_age=1)
                    return reqs
                else:
                    context['inactive'] = True
                    return render(request, 'account/login.html', context)
            else:
                # 比较失败，还在当前页面
                context['error'] = True
                return render(request, 'account/login.html', context)
        else:
            next_to = request.GET.get('next', '/')
            context['next_to'] = next_to
        return render(request, 'account/login.html', context)


# 退出
def logout_view(request):
    # 清理cookie里保存的username
    next_to = request.GET.get('next', '/')
    if next_to == '':
        next_to = '/'
    auth.logout(request)
    return redirect(next_to)


@login_required
def profile_view(request):
    return render(request, 'oauth/profile.html')


@login_required
@csrf_exempt
def change_profile_view(request):
    if request.method == 'POST':
        # 上传文件需要使用request.file
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '个人信息更新成功！')
            return redirect('accounts:profile')
        else:
            # 不是POST请求就返回空表单
            form = ProfileForm(instance=request.user)
        return render(request, 'oauth/change_profile.html', context={'form': form})
