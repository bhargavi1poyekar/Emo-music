from django.shortcuts import render,redirect,HttpResponse
from django.views import View

from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

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




