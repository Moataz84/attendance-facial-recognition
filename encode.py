from face_recognition import face_encodings, load_image_file
from json import load, dump

def encode_data():
  f = open("data/list.json")
  data = load(f)
  filtered_data = list(filter(lambda e: len(e["imgs"]) != 0, data))
  encoded = []

  for e in filtered_data:
    id = e["id"]
    name = e["name"]
    imgs = e["imgs"]    
    encodings = []
    for img in imgs:
      encoding = face_encodings(load_image_file(f"public/imgs/{img}"))[0].tolist()
      encodings.append(encoding)
    encoded.append({"id": id, "name": name, "encodings": encodings})
 
  f.close()

  with open("data/encoded.json", "w") as file:
    dump(encoded, file, indent=2)
    file.close()

encode_data()