from flask import Flask, render_template, request, redirect, Response, send_from_directory
import cv2

app = Flask(__name__)

global is_streaming
is_streaming = False
# poly = [(0,0),(960,0),(960,540),(0,540)]

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        # frame = cv2.resize(frame, (960, 540))

        if not success:
            break
        else:
            _, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

# TODO
# def capture():
#     return "Captured"

@app.route("/")
def index():
    return render_template("index.html", is_streaming=is_streaming)

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