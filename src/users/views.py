from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect


def login(request):
    """
    Logs in a user
    :param request: HttpRequest object
    :return:  HttpResponse object
    """
    context = dict()
    if request.method == 'POST':
        username = request.POST.get('usr')
        password = request.POST.get('pwd')
        user = authenticate(username=username, password=password)

        if user:
            # Authenticated user
            django_login(request, user)
            url = request.GET.get('next', 'user_blog')
            return redirect(url, username=username)
        else:
            # Non authenticated user
            context['error'] = "Wrong username / password"

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
