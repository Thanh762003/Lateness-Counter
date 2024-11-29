from flask import Flask, render_template, redirect, Response, request
from person_detection import HumanCount
import base64
import cv2

app = Flask(__name__)

global is_streaming
is_streaming = False
# poly = [(0,0),(960,0),(960,540),(0,540)]

# TODO
# def capture():
#     return "Captured"

def generate_frames():
    counter = HumanCount("yolov9c.pt")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = counter.show(frame)
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/")
def index():
    return render_template("index.html", is_streaming=is_streaming)

@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    org_img = None
    encoded_img = None
    count = 0
    if request.method == "POST":
        img_file = request.files["uploaded-img"]
        img_bin = img_file.read()
        counter = HumanCount("yolov9c.pt")
        encoded_img, count = counter.imshow(img_bin)
        org_img = base64.b64encode(img_bin).decode('utf-8')
    return render_template("upload.html", org_img=org_img, encoded_img=encoded_img, count=count)

@app.route("/toggle-stream", methods=["POST"])
def toggle_stream():
    global is_streaming
    is_streaming = not is_streaming
    return redirect("/")

@app.route("/stream")
def stream():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug=True)
