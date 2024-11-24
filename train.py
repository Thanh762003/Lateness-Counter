from ultralytics import YOLO

model = YOLO("yolov9c.pt")

model.train(data="desk/data.yaml", epochs=30, imgsz=640)
