from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def login(request: HttpRequest) -> HttpResponse:
    """Login page."""
    next_url = request.GET.get('next') or request.POST.get('next') or '/'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user_login(request, user)
            return redirect(next_url)
        messages.error(request, 'Invalid email or password.')

    return render(request, 'users/login.html')


def logout(request: HttpRequest) -> HttpResponse:
    """Log user out and redirect to login."""
    user_logout(request)
    return redirect(settings.LOGIN_URL)
