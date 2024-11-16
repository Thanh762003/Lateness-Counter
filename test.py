import mediapipe as mp
import cv2

cap = cv2.VideoCapture(0)
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while True:
        ret, img = cap.read()
        if not ret:
            break

        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if results.detections:
            for detection in results.detections:
                box = detection.location_data.relative_bounding_box
                x1, y1 = int(box.xmin * img.shape[1]), int(box.ymin * img.shape[0])
                x2, y2 = int((box.xmin + box.width) * img.shape[1]), int((box.ymin + box.height) * img.shape[0])
                img = cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)

        cv2.imshow("counter", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()