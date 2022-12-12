import numpy as np
import cv2 as cv
import time

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0

#cap.set(cv.CAP_PROP_FRAME_WIDTH, 150)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 200)

fps_count = []

while True:

    _, frame = cap.read()

    

    if(type(frame) == type(None) or _ == False):
        pass
   

    # font which we will be using to display FPS
    font = cv.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()

    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
 
    # converting the fps into integer
    fps = int(fps)
 
    fps_count.append(fps)
 
    # converting the fps to string so that we can display it on frame
    # by using putText function
    fps = str(fps)
 


    try:
        cv.imshow("window", frame)
      
    except Exception as e:
        print(str(e))

    if cv.waitKey(1) == ord('q'):

        break
print("average:")

print(int(sum(fps_count) / len(fps_count)))
cap.release()

cv.destroyAllWindows()

