from tensorflow.keras.models import model_from_json,load_model
import numpy as np
import tensorflow as tf
import cv2
from django.shortcuts import render,redirect,HttpResponse

class FacialExpressionModel(object):
    EMOTION_LIST = ["Happy" ,"Neutral" ,"Sad"]
    emotion_output = None
    IMG_SIZE = 256

    def __init__(self,model_json_file,model_weights_file,img_file):

        # Loading Model
        with open(model_json_file,"r") as json_file:
            loaded_model_in_json = json_file.read() 
            self.model = model_from_json(loaded_model_in_json)
            self.model.load_weights(model_weights_file)

        # Loading Image
        self.image = cv2.imread(img_file)

        # Loading FaceDetector
        self.face_cascade = cv2.CascadeClassifier("emotion/haarcascade_frontalface_default.xml")
          
        
    
    def preprocessImg(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        roi_img = None

        ## Detecting Face 
        try:
            faces = self.face_cascade.detectMultiScale(self.image,1.3,5)
            if len(faces)==0:
                print(f"No Face detected for given image ,Try again with new img :(")
                return 0,None
            elif len(faces)>1:
                print(f"Multiple Faces detected for given image ,Try again with new img :(")
                return 2,None
            else:
                for (x,y,w,h) in faces:
                    roi_img = self.image[y:y+h, x:x+w]

                roi_img = cv2.resize(roi_img,(self.IMG_SIZE,self.IMG_SIZE))
                roi_img = roi_img/255.0

        except Exception as _:
            print("An Error Ocurred, Please Try Again :(")
            return 3,None
        else:
            return True,roi_img

        
    def predictEmotion(self,roi_img):
        try:
            labels =  ["happy","neutral","sad"]
            prediction = self.model.predict(roi_img.reshape(1,self.IMG_SIZE,self.IMG_SIZE,3))
            
            self.emotion_output = labels[np.argmax(prediction)]

        except Exception as _:
            print("An Error Ocurred, Please Try Again :(")
            return False
        else:
            return True


    def getEmotions(self):
        return self.emotion_output

