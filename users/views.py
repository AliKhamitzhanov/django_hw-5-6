from django.shortcuts import render, get_object_or_404, redirect
from users.forms import RegisterForm, LoginForm, SetPassForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from posts.views import get_user_from_request
from django.views.generic import ListView, CreateView


def personal_info(request):
    if request.method == 'GET':
        if get_user_from_request(request):
            return render(request, 'users/personal.html', context={'user': request.user})
        else:
            return redirect('/')


class PersonalView(ListView):
    template_name = 'users/personal.html'

    def get(self, request, **kwargs):
        if get_user_from_request(request):
            return render(request, self.template_name, context={'user': request.user})
        else:
            return redirect('/')


class RegisterView(ListView, CreateView):
    template_name = 'users/reg_user.html'
    form_class = RegisterForm

    def get(self, request, *args):
        return render(request, self.template_name, context={
            'form': self.form_class
        })

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
                email=form.cleaned_data.get('email'),
                is_active=not False
            )
            return redirect('/users/login/')
        else:
            return render(request, self.template_name, context={
                'form': form
            })
# def register_view(request):
#     if request.method == 'GET':
#         return render(request, "users/reg_user.html", context={'form': RegisterForm})
#
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#
#         if form.is_valid():
#             User.objects.create_user(
#                 username=form.cleaned_data.get('username'),
#                 email=form.cleaned_data.get('email'),
#                 password=form.cleaned_data.get('password'),
#                 first_name=form.cleaned_data.get('first_name'),
#                 last_name=form.cleaned_data.get('last_name'),
#             )
#             return redirect("/users/login/")
#
#         else:
#              return render(request, 'users/reg_user.html', context={'form': form})


class ChangePass(ListView, CreateView):
    template_name = 'users/change.html'
    form_class = SetPassForm
    queryset = User.objects.all()

    def post(self, pk, request, *args, **kwargs):
        form = self.form_class(request.POST)
        instance = get_object_or_404(self.queryset, pk=pk)
        if form.is_valid():
            instance.set_password(form.cleaned_data.get('password'))
            instance.save()
            return redirect('/')
        else:
            return render(request, self.template_name, context={
                'form': self.form_class,
                'pk': pk
            })
# def set_password(request, id):
#     if request.method == 'GET':
#         return render(request, 'users/change.html', context={
#             'pers': SetPassForm,
#             'id': id
#         })
#     elif request.method == 'POST':
#         form = SetPassForm(request.POST)
#         user = User.objects.get(id=id)
#         if form.is_valid():
#             user.set_password(form.cleaned_data.get('password'))
#             user.save()
#             return redirect('/')
#         else:
#             return render(request, 'users/change.html', context={
#                 'pers': SetPassForm,
#                 'id': id
#             })


class LoginView(ListView, CreateView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request, *args):
        return render(request, self.template_name, context={'form': self.form_class})

    def post(self, request, *args, **kwargs):
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
            return render(request, self.template_name, context={'form': form})
# def login_view(request):
#     if request.method == "GET":
#         return render(request, 'users/login.html', context={'form': LoginForm})
#
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#
#         if form.is_valid():
#             user = authenticate(
#                 username=form.cleaned_data.get('username'),
#                 password=form.cleaned_data.get('password')
#             )
#             if user:
#                 login(request, user)
#                 return redirect('/')
#
#         else:
#             return render(request, 'users/login.html', context={'form': form})


class LogoutView(ListView):
    def get(self, request, *args):
        logout(request)
        return redirect('/')

# def logout_view(request):
#     if request.method == 'GET':
#         logout(request)
#         return redirect('/')

