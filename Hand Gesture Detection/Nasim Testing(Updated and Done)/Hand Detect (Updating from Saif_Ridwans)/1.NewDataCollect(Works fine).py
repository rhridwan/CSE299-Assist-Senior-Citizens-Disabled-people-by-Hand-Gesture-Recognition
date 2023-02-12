import cv2
import numpy as np
import os
#it is like creating folder
if not os.path.exists("data"):
    os.makedirs("data")
    os.makedirs("data/train")
    os.makedirs("data/test")
    os.makedirs("data/train/emergency1")
    os.makedirs("data/train/emergency2")
    os.makedirs("data/train/normal_emergency")
    os.makedirs("data/train/background")
    os.makedirs("data/train/deaf emergency")
#    os.makedirs("data/train/like")
#    os.makedirs("data/train/rock")

# Train directory loaded
directory = 'data/train/'
cap = cv2.VideoCapture(0) #it is like my webcam is activated

while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)
    
       # Getting count of existing images
    count = {'E1': len(os.listdir(directory+"/emergency1")),
             'E2': len(os.listdir(directory+"/emergency2")),
             'NE': len(os.listdir(directory+"/normal_emergency")),
             'BD': len(os.listdir(directory+"/background")),
             'DE': len(os.listdir(directory+"/deaf emergency")),
#             'Rock': len(os.listdir(directory+"/rock"))
             }
             
    
      # Printing the count in each set to the screen
    cv2.putText(frame, "MODE : TRAIN", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    cv2.putText(frame, "IMAGE COUNT:", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    cv2.putText(frame, "EmergencyOne: "+str(count['E1']), (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    cv2.putText(frame, "EmergencyTwo: "+str(count['E2']), (10, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    cv2.putText(frame, "Normal: "+str(count['NE']), (10, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    cv2.putText(frame, "BACKGROUND : "+str(count['BD']), (10, 180), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1)
    cv2.putText(frame, "Deaf Emergency : "+str(count['DE']), (10, 200), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
#    cv2.putText(frame, "ROCK : "+str(count['Rock']), (10, 220), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    
    
    # Coordinates of the ROI
    x1 = int(0.6*frame.shape[1])
    y1 = 80
    x2 = frame.shape[1]-80
    y2 = int(0.4*frame.shape[1])
    # Drawing the ROI
    # The increment/decrement by 1 is to compensate for the bounding box
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (0,255,0) ,2)
    # Extracting the ROI
    roi = frame[y1:y2, x1:x2]
    roi = cv2.resize(roi, (350, 350))#SIZE OF ROI THE LITTLE GRAYSCALE WINDOW
    
    cv2.imshow("Frame", frame)
    
    # Changing into GryScale
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Getting Binary Image
    _, roi = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("ROI", roi)
    
    interrupt = cv2.waitKey(10)
    
    # esc key
    if interrupt & 0xFF == 32: 
        break
    
    #captures from the frame
    if interrupt & 0xFF == ord('q'): 
            cv2.imwrite(directory+'emergency1/'+str(count['E1'])+'.jpg', roi)
    if interrupt & 0xFF == ord('w'):    
            cv2.imwrite(directory+'emergency2/'+str(count['E2'])+'.jpg', roi)
    if interrupt & 0xFF == ord('e'): 
            cv2.imwrite(directory+'normal_emergency/'+str(count['NE'])+'.jpg', roi)
    if interrupt & 0xFF == ord('b'):   
            cv2.imwrite(directory+'background/'+str(count['BD'])+'.jpg', roi)
    if interrupt & 0xFF == ord('d'):
            cv2.imwrite(directory+'deaf emergency/'+str(count['DE'])+'.jpg', roi)
#    if interrupt & 0xFF == ord('r'):
#            cv2.imwrite(directory+'rock/'+str(count['Rock'])+'.jpg', roi)
    
cap.release()
cv2.destroyAllWindows()
    