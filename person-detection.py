# import cv2
from ultralytics import YOLO

model = YOLO("yolov9c.pt")

model.predict("static/images/classroom-1.jpg", imgsz=1280, conf=0.4, save=True)
