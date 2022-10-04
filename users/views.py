from django.shortcuts import render
from users.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    if request.method == 'GET':
        return render(request, "users/reg_user.html", context={'form': RegisterForm})

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'),
            )
            return redirect("/users/login/")

        else:
            return render(request, 'users/reg_user.html', context={'form': form})


def login_view(request):
    if request.method == "GET":
        return render(request, 'users/login.html', context={'form': LoginForm})

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('/')

        else:
            return render(request, 'users/login.html', context={'form': form})


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/')