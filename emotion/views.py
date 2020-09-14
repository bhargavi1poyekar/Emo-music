from django.shortcuts import render,HttpResponse
from . import emotion_model 
from PIL import Image
# Create your views here.

def emotion(request):
    JSON_PATH = "/home/pritamrao/Desktop/TE-SEM-5-6/projects/music/emotion/model.json"
    WEIGHTS = "/home/pritamrao/Desktop/TE-SEM-5-6/projects/music/emotion/model_weights.h5"
    IMG = "/home/pritamrao/Desktop/TE-SEM-5-6/projects/music/static/images/surprise.webp"

    fer = emotion_model.FacialExpressionModel(JSON_PATH,WEIGHTS,IMG)
    emotion = fer.predict_emotion()

    context = {'emotion':emotion}


    return render(request,'emotion/index.html',context)
    #return HttpResponse("hello")