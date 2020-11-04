from django.shortcuts import render,HttpResponse
from . import emotion_model 
from Image.models import Image
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# Create your views here.

def emotion(request):
    JSON_PATH = str(BASE_DIR)+"/emotion/model_config.json"
    WEIGHTS_PATH = str(BASE_DIR)+"/emotion/model_wts.h5"
    
    ## Getting ImgPath
    image = Image.objects.get(user=request.user)
    image_url = image.Image_url
    IMG_PATH = str(BASE_DIR)+"/media/"+str(image_url)


    fer = emotion_model.FacialExpressionModel(JSON_PATH,WEIGHTS_PATH,IMG_PATH)
    return_val,processed_img = fer.preprocessImg()

    emotion = ""
    if return_val:
        success = fer.predictEmotion(processed_img)
        if success:
            emotion += fer.getEmotions()
            print(f'\n\n\nEMOTION IS {emotion}\n\n\n')

            ## After succesful removal of emotion delete the image
            image.delete()
    else:
        print("PreProcess me error")

    context = {'emotion':emotion,'image':image_url}
    return render(request,'emotion/index.html',context)