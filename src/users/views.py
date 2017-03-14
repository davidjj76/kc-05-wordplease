from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm


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
                django_login(request, user)
                url = request.GET.get('next', 'user_blog')
                return redirect(url, username=username)
            else:
                # Non authenticated user
                context['error'] = "Wrong username / password"

        context['form'] = form
        return render(request, 'login.html', context)


def logout(request):
    """
    Logs out a user
    :param request: HttpRequest object
    :return:  HttpResponse object
    """
    django_logout(request)
    return redirect('login')


def signup(request):
    return render(request, 'signup.html')
