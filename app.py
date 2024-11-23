from flask import Flask, render_template, request, redirect, Response, send_from_directory
import cv2

app = Flask(__name__)

global is_streaming
is_streaming = False

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()

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
    hour_start = request.form["hour-start"]
    minute_start = request.form["minute-start"]
    hour_end = request.form["hour-end"]
    minute_end = request.form["minute-end"]
    interval = request.form["interval"]

    print(f"Class starts at: {hour_start}:{minute_start}")
    print(f"Class ends at: {hour_end}:{minute_end}")
    print(f"Take snapshot every interval: {interval}")

    global is_streaming
    is_streaming = not is_streaming

    return redirect("/")

@app.route("/stream")
def stream():
    if is_streaming:
        return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
    return send_from_directory("static", "images/starting-soon.jpg")

if __name__ == "__main__":
    app.run(debug=True)