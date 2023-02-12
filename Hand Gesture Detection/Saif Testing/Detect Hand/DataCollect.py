import cv2
import numpy as np
import os
#it is like creating folder
if not os.path.exists("data"):
    os.makedirs("data")
    os.makedirs("data/train")
    os.makedirs("data/train/hi")
    os.makedirs("data/train/ok")
    os.makedirs("data/train/like")
    os.makedirs("data/train/rock")

# Train directory loaded
directory = 'data/train/'
cap = cv2.VideoCapture(0) #it is like my webcam is activated

while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)
    
       # Getting count of existing images
    count = {'Hi': len(os.listdir(directory+"/hi")),
             'Ok': len(os.listdir(directory+"/ok")),
             'Like': len(os.listdir(directory+"/like")),
             'Rock': len(os.listdir(directory+"/rock"))}
    
      # Printing the count in each set to the screen
    cv2.putText(frame, "MODE : TRAIN", (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    cv2.putText(frame, "IMAGE COUNT", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    cv2.putText(frame, "HI : "+str(count['Hi']), (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    cv2.putText(frame, "OK : "+str(count['Ok']), (10, 140), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    cv2.putText(frame, "LIKE : "+str(count['Like']), (10, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    cv2.putText(frame, "ROCK : "+str(count['Rock']), (10, 180), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    
    
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
    roi = cv2.resize(roi, (200, 200))#SIZE OF ROI THE LITTLE GRAYSCALE WINDOW
 
    cv2.imshow("Frame", frame)
    
    
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
    cv2.imshow("ROI", roi)
    
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27: # esc key
        break

    if interrupt & 0xFF == ord('h'):
        cv2.imwrite(directory+'hi/'+str(count['Hi'])+'.jpg', roi)
    if interrupt & 0xFF == ord('o'):
        cv2.imwrite(directory+'ok/'+str(count['Ok'])+'.jpg', roi)
    if interrupt & 0xFF == ord('l'):
        cv2.imwrite(directory+'like/'+str(count['Like'])+'.jpg', roi)
    if interrupt & 0xFF == ord('r'):
        cv2.imwrite(directory+'rock/'+str(count['Rock'])+'.jpg', roi)
    
cap.release()
cv2.destroyAllWindows()
    