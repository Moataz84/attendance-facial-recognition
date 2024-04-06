from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from os.path import abspath
from uuid import uuid4
from base64 import b64decode
from os import listdir, remove
from main import get_face_result

app = Flask(__name__, template_folder=abspath("./views"), static_folder="public")
socketio = SocketIO(app)   
@app.get("/")
def index():
  return render_template("index.html")

@socketio.on("get-image-id")
def get_image_id():
  image_id  = str(uuid4())
  emit("image-id", image_id)

@socketio.on("disconnect-client")
def disconnect_client(image_id):
  disconnect()
  for file in listdir("tmp"):
    if image_id in file:
      try:
        remove(f"tmp/{file}")
      except:
        return

@socketio.on("frame")
def receive_frames(data):
  frame = data["frame"]
  image_id = data["imageId"]
  header, file_data = frame.split(",", 1)
  image_path = f"tmp/{image_id}-{str(uuid4())}.jpg"
  with open(image_path, "wb") as f:
    f.write(b64decode(file_data))
  name = get_face_result(image_path)
  remove(image_path)
  emit("face-result", name)

if __name__ == "__main__":
  socketio.run(app, debug=True, host="0.0.0.0", port=5001, ssl_context=("SSL/cert.pem", "SSL/key.pem"))