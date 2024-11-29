import cv2
from ultralytics import YOLO
import numpy as np
import base64

class HumanCount:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.model.fuse()

    def _process_img(self, img, results):
        count = 0

        for result in results:
            # Filter out only boxes that identify human
            boxes = [x for x in result.boxes if x.conf[0] >= 0.4 and x.cls.cpu().numpy().astype(int) == 0]

            for box in boxes:
                [x1, y1, x2, y2] = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                count = len(boxes)

                color = (255, 0, 0)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f"person {box.conf[0]:.2f}", (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        _, buffer = cv2.imencode(".jpg", img)
        return buffer, count

    def show(self, frame):
        frame = cv2.resize(frame, (960, 540))
        results = self.model.track(frame, stream=True)
        buffer, count = self._process_img(frame, results)
        cv2.putText(frame, f"Attendance count: {count}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        return buffer.tobytes()

    def imshow(self, img_bin):
        file_bytes = np.frombuffer(img_bin, np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        results = self.model(img)
        buffer, count = self._process_img(img, results)
        return base64.b64encode(buffer).decode("utf-8"), count
