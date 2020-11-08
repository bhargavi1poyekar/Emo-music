from django.shortcuts import render,redirect,HttpResponse
from . import emotion_model 
from Image.models import Image
from playlists.models import Playlist,Playlist_songs
from songs.models import Song
from django.contrib.auth.models import User
from pathlib import Path
import random
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

    # Once image is available in FER class delete it from database
    image.delete()
    return_val,processed_img = fer.preprocessImg()
    
    if return_val=="noFace":
        error="No Face detected for given image ,Try again with new img :("
        return redirect("error-page",error)
    elif return_val=="mulFace":
        error="Multiple Face detected for given image ,Try again with new img :("
        return redirect("error-page",error)
    elif return_val=="exception":
        error="An Unkwon Error Ocurred, Please Try Again :("
        return redirect("error-page",error)

    emotion = ""
    if return_val:
        success = fer.predictEmotion(processed_img)
        if success:
            emotion += fer.getEmotions()
            print(f'\n\n\nEMOTION IS {emotion}\n\n\n')
            
    else:
        print("PreProcess me error")
    
    #context = {'emotion':emotion,'image':image_url}
    #####


    user_songs=Song.objects.filter(user=request.user).filter(emotion=emotion)
    admin =User.objects.filter(username='admin')[0]
    admin_songs=Song.objects.filter(user=admin).filter(emotion=emotion)
    
    ply=Playlist.objects.filter(user=admin).filter(playlist_name=request.user.username+'_'+emotion)
    print(ply)
    if ply :
        ply.delete()

    playlist=Playlist(user=admin,playlist_name=request.user.username+'_'+emotion,
                number_of_songs=-1)
    playlist.save()

    for song in user_songs:
        relation=Playlist_songs(playlist=playlist,song=song)
        relation.save()
    sz=admin_songs.count()
    # print(sz)

    sampling = set(random.sample(list(range(0,sz)), k=min(10,sz)))
    i=0 
    order=[*range(sz)]
    random.shuffle(order)
    # print(user_songs)
    # print(admin_songs)
    # print(order,sampling)

    while i <sz :
        if order[i] in sampling:
            print(i,order[i],admin_songs[order[i]])
            relation=Playlist_songs(playlist=playlist,song=admin_songs[order[i]])
            relation.save()
        i+=1

    return redirect('displayPlaylist',playlist.id)
    ####
    
    
    
    
