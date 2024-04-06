from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from os.path import abspath
from uuid import uuid4
from base64 import b64decode

app = Flask(__name__, template_folder=abspath("./views"), static_folder="public")
socketio = SocketIO(app)   
@app.get("/")
def index():
  return render_template("index.html")

@socketio.on("get-video-id")
def get_video_id():
  video_id  = str(uuid4())
  emit("video-id", video_id)

@socketio.on("frame")
def receive_frames(data):
  frame = data["frame"]
  header, file_data = frame.split(",", 1)
  with open(f"tmp/{str(uuid4())}.jpg", "wb") as f:
    f.write(b64decode(file_data))

if __name__ == "__main__":
  socketio.run(app, debug=True, host="0.0.0.0", port=5001, ssl_context=("SSL/cert.pem", "SSL/key.pem"))