import cv2 as cv
import numpy as np
import config as conf

kernel = np.ones((1, 1), np.uint8)

for index in range(0, 10):
    path = r'C:\Users\david\Desktop\cvPics2\img'+ str(index) + r'.jpg'
    path_save = r'C:\Users\david\Desktop\cvPics\img1'+ str(index) + r'.jpg'

    frame_orig = cv.imread(path)
    frame_orig = cv.resize(frame_orig, (500, 500))
    black_img = np.zeros_like(frame_orig)

    white_img = cv.bitwise_not(black_img)

    frame_hsv = cv.cvtColor(frame_orig, cv.COLOR_BGR2HSV)

    mask_hsv = cv.inRange(frame_hsv, conf.green[0], conf.green[1])

    contours, _ = cv.findContours(mask_hsv, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv.contourArea)

    img_cont = cv.drawContours(white_img, [contour], -1, (0, 0, 0), -1)

    height, width = img_cont.shape[:2]
    img_cont_resized = cv.resize(img_cont, (int(img_cont.shape[1]/1.2), int(img_cont.shape[0]/1.2)))
    print(width, height)
    top = int((height - img_cont_resized.shape[0])/2)
    bottom = top
    left = int((width - img_cont_resized.shape[1])/2)
    right = left

    final_img = cv.copyMakeBorder(img_cont_resized, top, bottom, left, right, cv.BORDER_REPLICATE)

    green_part = cv.bitwise_or(frame_orig, final_img)

    x, y, w, h = cv.boundingRect(contour)

    img_draw_cropped = green_part[y:y+h, x:x+w]

    img_draw_cropped = cv.resize(img_draw_cropped, (192,192))

    cv.imwrite(path_save, img_draw_cropped)




