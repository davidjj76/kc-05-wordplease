from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm, SignupForm


def login_and_redirect(request, user):

    django_login(request, user)
    url = request.GET.get('next', 'user_blog')
    return redirect(url, username=request.user.username)


class LoginView(View):

    def get(self, request):
        """
        Shows login form
        :param request: HttpRequest object
        :return:  HttpResponse object
        """
        return render(request, 'login.html', { 'form': LoginForm() })

    def post(self, request):
        """
        Logs in a user
        :param request: HttpRequest object
        :return:  HttpResponse object
        """
        form = LoginForm(request.POST)
        context = dict()

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                # Authenticated user
                return login_and_redirect(request, user)
            else:
                # Non authenticated user
                context['error'] = "Wrong username / password"

        context['form'] = form
        return render(request, 'login.html', context)


class SignupView(View):

    def get(self, request):
        """
        Shows sign up form
        :param request: HttpRequest object
        :return:  HttpResponse object
        """
        return render(request, 'signup.html', {
            'form': SignupForm()
        })

    def post(self, request):
        """
        Signs up a new user
        :param request: HttpRequest object
        :return:  HttpResponse object
        """
        form = SignupForm(request.POST)
        context = dict()

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            if new_user:
                # User created
                return login_and_redirect(request, new_user)
            else:
                # Non created user
                context['error'] = "Error creating user"

        context['form'] = form
        return render(request, 'signup.html', context)


def logout(request):
    """
    Logs out a user
    :param request: HttpRequest object
    :return:  HttpResponse object
    """
    django_logout(request)
    return redirect('login')
