from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from users.models import *
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request,'users/index.html')
    return redirect('login')

def login(request):
    return render(request,'users/login.html')

def createUser(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

def deleteUser(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        user.delete()
        return redirect('logout')
    

def showProfile(request):
    if request.user.is_authenticated:
        return render(request,'users/profile.html')

def editProfile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            profile=Profile.objects.get(user=request.user)
            profile.phone_number=request.POST['phone_number']
            profile.bio=request.POST['bio']
            profile.save()
            return redirect('user-profile')
        else:
            return render(request,'users/edit-profile.html')



