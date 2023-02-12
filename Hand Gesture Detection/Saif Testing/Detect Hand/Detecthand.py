import numpy as np
from keras.models import model_from_json
from firebase import firebase
import operator
import cv2
import sys, os


firebase = firebase.FirebaseApplication('https://assist-5d80b.firebaseio.com/', None)
# Loading the model
json_file = open("model-bw.json", "r")
model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(model_json)
# load weights into new model
loaded_model.load_weights("model-bw.h5")
print("Loaded model from disk")

cap = cv2.VideoCapture(0)

# Category dictionary
#categories = {'hi': 'Hello there', 'like': 'I like you', 'ok': 'Its Coool', 'rock': 'We will Rock You'}
while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)
    
    # Got this from collect-data.py
      
    # Coordinates of the ROI
    x1 = int(0.6*frame.shape[1])
    y1 = 80
    x2 = frame.shape[1]-80
    y2 = int(0.4*frame.shape[1])
    # Drawing the ROI
    # The increment/decrement by 1 is to compensate for the bounding box
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (0,0,255) ,2)
    # Extracting the ROI
    roi = frame[y1:y2, x1:x2]
     
    # Resizing the ROI so it can be fed to the model for prediction
    roi = cv2.resize(roi, (64, 64)) 
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, test_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("test", test_image)
    
    
    # Batch of 1
    result = loaded_model.predict(test_image.reshape(1, 64, 64, 1))
    prediction = {'Hello There': result[0][0], 
                  'You deserve a Like': result[0][1], 
                  'Everything is ok': result[0][2],
                  'We will rock you': result[0][3]}
    # Sorting based on top prediction
    prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    
    # Displaying the predictions
    cv2.putText(frame, prediction[0][0], (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (225,0,0), 1)    
    cv2.imshow("Frame", frame)
    firebase.put('/Status/Values','STATUS',prediction[0][0])

    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break
        
 
cap.release()
cv2.destroyAllWindows()