from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from Image.models import *
from django.contrib.auth.models import User

# Create your views here.

def image(request):
    return render(request,'Image/ImageUpload.html')

def takeImage(request):
    if request.method=="GET":
        return render(request,'Image/Upload.html')
    else:
        image=request.FILES['emo-image']
        emo_image=Image(user=request.user,Image_url=image)
        emo_image.save()
        return redirect('filterImage')

# def useCamera(request):
#     if request.method=="GET":
#         return render(request,'Image/CaptureImage.html')
#     else:
#         return redirect('filterImage')

def filterImage(request):
    return redirect('emotion')
        



