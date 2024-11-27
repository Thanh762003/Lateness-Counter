import cv2
from ultralytics import YOLO

class HumanCount:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.model.fuse()

    def show(self, frame):
        frame = cv2.resize(frame, (960, 540))
        results = self.model.track(frame, stream=True)

        for result in results:
            # Filter out only boxes that identify human
            boxes = [x for x in result.boxes if x.conf[0] >= 0.4 and x.cls.cpu().numpy().astype(int) == 0]

            for box in boxes:
                [x1, y1, x2, y2] = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                color = (255, 0, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f'person {box.conf[0]:.2f}', (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(frame, f'Attendance count: {len(boxes)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        return frame
