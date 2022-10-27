from cmath import inf
from unicodedata import name
import cv2 as cv
import pandas as pd
import numpy as np

sclicked = False
dclicked = False

index=["color","color_name","hex","R","G","B"] #create data set with rgb colors
csv = pd.read_csv('colors.csv', names=index, header=None)

def saveImage(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN: #single click activation
        global sclicked
        sclicked = True

xval = yval = r = g = b = 0
def saveColor(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK: #double click activation
        global dclicked, xval, yval
        dclicked = True
        xval = x
        yval = y


def nameColor(r, g, b):
    minimum = float(inf)
    for i in range(len(csv)):
        d = abs(r - int(csv.loc[i, 'R'])) + abs(g - int(csv.loc[i,'G'])) + abs(b - int(csv.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            name = csv.loc[i, 'color_name']
    return name


def processShot(frame):
    b,g,r = frame[yval, xval]
    b = int(b)
    g = int(g)
    r = int(r)

    output = nameColor(r, g, b)
    return (output, r, g, b)

capture = cv.VideoCapture(0)

if (capture.isOpened() == False):
    print("Error")

cv.namedWindow('Video')
cv.namedWindow('Captured_Image')
cv.setMouseCallback('Captured_Image', saveColor) #functions when screenshot is taken
cv.setMouseCallback('Video', saveImage) #functions when video playback occurs
while(capture.isOpened()):
    status, frame = capture.read()
    if status == True:
        if sclicked:
            sclicked = False
            img = frame
            cv.imshow('Captured_Image', img)
        if dclicked:
            copy = img.copy()
            output, r, g, b = processShot(img)
            cv.putText(copy, output, (50, 50), 3, 1, (r, g, b), 2, cv.LINE_AA)
            cv.imshow('Captured_Image', copy)
            dclicked = False
                
        cv.imshow('Video', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
cv.destroyAllWindows

        
