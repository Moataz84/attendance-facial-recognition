from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from base64 import b64decode
from os.path import abspath
from os import remove
from json import load
from compare import get_face_result

app = Flask(__name__, template_folder=abspath("./views"), static_folder="public")
socketio = SocketIO(app)#, logger=True)

@app.get("/")
def index():
  return render_template("index.html")

@socketio.on("frame")
def receive_frame(data):
  frame = data["frame"]
  image_id = data["imageId"]
  _, file_data = frame.split(",", 1)
  image_path = f"tmp/{image_id}.jpg"
  with open(image_path, "wb") as f:
    f.write(b64decode(file_data))
  id, name = get_face_result(image_path)
  emit("face-result", {"id": id, "name": name})

@socketio.on("disconnect-client")
def disconnect_client(image_id):
  disconnect()
  try:
    remove(f"tmp/{image_id}.jpg")
  except:
    return
  
@socketio.on("check-present")
def mark_present(id):
  f = open("data/present.json")
  data = load(f)
  f.close()
  person = list(filter(lambda e: e["id"] == id, data))[0]
  if not person["present"]:
    emit("present", person)
  

if __name__ == "__main__":
  socketio.run(app, debug=True, host="0.0.0.0", port=5001, ssl_context=("SSL/cert.pem", "SSL/key.pem"))