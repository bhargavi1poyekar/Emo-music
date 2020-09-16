# from tensorflow.keras.models import model_from_json
# import numpy as np
# import tensorflow as tf
# import cv2

# class FacialExpressionModel(object):
#     EMOTION_LIST = ["Angry" ,"Disgust" ,"Fear" ,"Happy","Sad","Surprise","Neutral"]

#     def __init__(self,model_json_file,model_weights_file,img):
#         with open(model_json_file,"r") as json_file:
#             loaded_model_in_json = json_file.read() 
#             self.loaded_model = model_from_json(loaded_model_in_json)

#         self.image = cv2.imread(img)
#         self.image = cv2.resize(self.image,(48,48))  
#         self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
#         #cv2.imshow("image",self.image)
#         #print(self.image.shape)
#         self.loaded_model.load_weights(model_weights_file)

#         #print("\n\n\n\n")
#         #print(self.loaded_model.summary())


#     def predict_emotion(self):
#         ## Image reshaping wala part dekh lena

#         input_img = self.image/255
#         input_img = input_img.reshape((1,48,48,1))
#         self.preds = self.loaded_model.predict(input_img)

#         return self.EMOTION_LIST[np.argmax(self.preds)]


