import mediapipe as mp
import cv2

cap = cv2.VideoCapture(0)
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while True:
        ret, img = cap.read()

        if not ret:
            break

        img = cv2.resize(img, (960, 540))
        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        cnt = 0

        if results.detections:
            cnt = len(results.detections)

        cv2.putText(img, f'Attendance count: {cnt}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow("counter", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()