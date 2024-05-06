from django.shortcuts import render, redirect
from users.models import *
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from typing import Union


# Create your views here.
def get_home(request: HttpRequest) -> Union[HttpResponse, redirect]:
    """
    View function to render the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Union[HttpResponse, redirect]: Renders the index page if user is authenticated,
        otherwise redirects to login.
    """
    if request.user.is_authenticated:
        return render(request, 'users/index.html')
    return redirect('login')


def login(request: HttpRequest) -> HttpResponse:
    """
    View function to render the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the login page.
    """
    return render(request, 'users/login.html')


def create_user(request: HttpRequest) -> Union[HttpResponse, render]:
    """
    View function to handle user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Union[HttpResponse, render]: Renders the registration page with form, or redirects
        to login on successful registration.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def delete_user(request: HttpRequest) -> HttpResponse:
    """
    View function to delete user account.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to logout after deleting the user account.
    """
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        user.delete()
        return redirect('logout')
    

def show_profile(request: HttpRequest) -> HttpResponse:
    """
    View function to render user profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the user profile page.
    """
    if request.user.is_authenticated:
        return render(request, 'users/profile.html')


def edit_profile(request: HttpRequest) -> Union[HttpResponse, render]:
    """
    View function to edit user profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Union[HttpResponse, render]: Renders the edit profile page with form, or redirects to user profile on successful edit.
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            profile = Profile.objects.get(user=request.user)
            profile.phone_number = request.POST['phone_number']
            profile.bio = request.POST['bio']
            profile.save()
            return redirect('user-profile')
        else:
            return render(request, 'users/edit-profile.html')


def show_error(request: HttpRequest, error: str) -> HttpResponse:
    """
    View function to render error page.
    Args:
        request (HttpRequest): The HTTP request object.
        error (str): The error message to display.
    Returns:
        HttpResponse: Renders the error page with the provided error message.
    """
    return render(request, 'users/error-page.html', {'error': error})
