import time
from turtle import left
import cv2
from tkinter import Image
from PIL import ImageGrab
import pyautogui
import keyboard
from pynput.mouse import Listener
import mouse

import win32api
import time
from pynput.mouse import Button, Controller
mouse = Controller()

import numpy as np

COLORS = [(0,255,255),(255,255,0),(0,255,0),(255,0,0)]

class_names = []

with open("coco.names","r") as f:
    class_names  = [cname.strip() for cname  in f.readlines() ]
    
cap = cv2.VideoCapture()
#cap = ImageGrab.grab(bbox=(0,0,1200,1000))
#cap = pyautogui.screenshot()
#cap = cv2.VideoCapture("Fontal.MP4")

net = cv2.dnn.readNet("yolov4-tiny.weights","yolov4-tiny.cfg")

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416,416),scale=1/255)


def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            return True

while True:

    cap = ImageGrab.grab(bbox=(0,0,1200,1000))
    #_, frame = cap.read()
    frame = np.array(cap)

    start = time.time()

    classes , scores , boxes = model.detect(frame, 0.1, 0.2)

    end = time.time()

    for(classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]

        label = f'{class_names[classid]} : {score}'

        if classid == 0:
            if win32api.GetAsyncKeyState(0x01):
                x, y = win32api.GetCursorPos()
                print(x, y)
                print(box[0]+(box[2]-10))
                if x >= (box[0]-100) and x <= (box[0]+(box[2]+100)) and y >= (box[1]-100) and y <= (box[1]+(box[3]+100)):
                    pyautogui.moveTo(box[0]+(box[2]/2),box[1]+(box[3]/4))
                    print("moveu")
               # else:
                 #   pass
           
                #pyautogui.moveTo(box[0]+(box[2]/2),box[1]+(box[3]/2))
                #print(box)

        cv2.rectangle(frame, box, color, 2)

        cv2.putText(frame,label, (box[0],box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    fps_label = f"FPS: {round((1.0/(end - start)),2)}"  

    cv2.putText(frame, fps_label, (0, 25),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),5)
    cv2.putText(frame, fps_label, (0, 25),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),3)
    
    cv2.imshow("detections", frame)


    if cv2.waitKey(1) == 27:
        break

cap.realese()
cv2.destroyAllWindows()
