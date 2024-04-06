from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from os.path import abspath, join
from uuid import uuid4
from base64 import b64decode
from os import listdir, remove
import cv2

app = Flask(__name__, template_folder=abspath("./views"), static_folder="public")
socketio = SocketIO(app)   
@app.get("/")
def index():
  return render_template("index.html")

@socketio.on("get-video-id")
def get_video_id():
  video_id  = str(uuid4())
  emit("video-id", video_id)

@socketio.on("disconnect-client")
def disconnect_client(video_id):
  disconnect()
  for file in listdir("tmp"):
    if video_id in file:
      try:
        remove(f"tmp/{file}")
      except:
        return

@socketio.on("frame")
def receive_frames(data):
  frame = data["frame"]
  videoId = data["videoId"]
  header, file_data = frame.split(",", 1)
  with open(f"tmp/{videoId}-{str(uuid4())}.jpg", "wb") as f:
    f.write(b64decode(file_data))
  images = [img for img in listdir("tmp") if (videoId in img and img.endswith(".jpg"))]
  frame = cv2.imread(join("tmp", images[0]))
  height, width, layers = frame.shape
  video = cv2.VideoWriter(f"tmp/{videoId}.avi", 0, 1, (width, height))
  for image in images:
    video.write(cv2.imread(join("tmp", image)))

  cv2.destroyAllWindows()
  video.release()

if __name__ == "__main__":
  socketio.run(app, debug=True, host="0.0.0.0", port=5001, ssl_context=("SSL/cert.pem", "SSL/key.pem"))