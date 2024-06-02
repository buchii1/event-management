from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.urls import reverse_lazy

from .forms import NewUserForm, UserLoginForm

userModel = get_user_model()


def register(request):
    """
    Register a new user.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: Redirects to the user's profile page if registration is successful, 
        otherwise renders the registration form.
    """
    if request.method == 'POST':
        form = NewUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (f"Account created for <b>{username}</b>."))
            return redirect('main:profile', username=username)
    else:
        form = NewUserForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_request(request):
    """
    Login an existing user.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: Redirects to the next URL if login is successful,
        otherwise renders the login form.
    """
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', reverse_lazy('main:profile', kwargs={'username': username}))
                return redirect(next_url)
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_request(request):
    """
    Logout the current user.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: Redirects to the home page after logout.
    """
    logout(request)
    return redirect('main:index')