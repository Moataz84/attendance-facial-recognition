from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from base64 import b64decode
from os.path import abspath
from os import remove
from json import load, dump
from compare import get_face_result
from time import time
from datetime import datetime

app = Flask(__name__, template_folder=abspath("./views"), static_folder="public")
socketio = SocketIO(app)#, logger=True)

def format_entry(person):
  if not person["present"]:
    return person
  signed_time = datetime.fromtimestamp(person["time"]).strftime("%H:%M %p")  

  return {
    "id": person["id"], 
    "name": person["name"], 
    "profile": person["profile"], 
    "present": True, 
    "time": signed_time
  }

@app.get("/read")
def reader():
  f = open("data/present.json")
  result = load(f)
  data = list(map(format_entry, result))
  f.close()
  return render_template("reader.html", data=data)

@app.get("/")
def index():
  f = open("data/present.json")
  result = load(f)
  data = list(map(format_entry, result))
  f.close()
  return render_template("index.html", data=data)

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
  person = list(filter(lambda e: e["id"] == id, data))[0]
  if not person["present"]:
    signed_time = time()
    present = list(map(lambda e: e 
      if not e["id"] == id 
      else {"id": e["id"], "name": e["name"], "profile": e["profile"], "present": True, "time": signed_time}, data)
    )
    with open("data/present.json", "w") as file:
      dump(present, file, indent=2)
      file.close()
    emit("mark-present", person)
    socketio.emit("show-person", person["id"])
  f.close()
  
@socketio.on("signout")
def signout(id):
  f = open("data/present.json")
  data = load(f)
  socketio.emit("signedout", id)
  present = list(map(lambda e: e 
    if not e["id"] == id 
    else {"id": e["id"], "name": e["name"], "profile": e["profile"], "present": False, "time": None}, data)
  )
  with open("data/present.json", "w") as file:
    dump(present, file, indent=2)
    file.close()
  f.close()

if __name__ == "__main__":
  socketio.run(app, debug=True, host="0.0.0.0", port=5001, ssl_context=("SSL/cert.pem", "SSL/key.pem"))