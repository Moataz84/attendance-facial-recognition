from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from os.path import abspath
from base64 import b64decode
from os import remove
from compare import get_face_result

app = Flask(__name__, template_folder=abspath("./views"), static_folder="public")
socketio = SocketIO(app, logger=True)

@app.get("/")
def index():
  return render_template("index.html")

@socketio.on("disconnect-client")
def disconnect_client(image_id):
  disconnect()
  try:
    remove(f"tmp/{image_id}.jpg")
  except:
    return

@socketio.on("frame")
def receive_frame(data):
  frame = data["frame"]
  image_id = data["imageId"]
  _, file_data = frame.split(",", 1)
  image_path = f"tmp/{image_id}.jpg"
  with open(image_path, "wb") as f:
    f.write(b64decode(file_data))
  name = get_face_result(image_path)
  emit("face-result", name)

if __name__ == "__main__":
  socketio.run(app, debug=True, host="0.0.0.0", port=5001, ssl_context=("SSL/cert.pem", "SSL/key.pem"))