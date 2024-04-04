from face_recognition import face_encodings, load_image_file
from json import load, dump

def encode_data():
  f = open("data.json")
  data = load(f)
  filtered_data = list(filter(lambda e: len(e["imgs"]) != 0, data))
  encoded = []

  for e in filtered_data:
    encodings = []
    imgs = e["imgs"]
    name = e["name"]
    for img in imgs:
      encoding = face_encodings(load_image_file(f"images/{img}"))[0].tolist()
      encodings.append(encoding)
    encoded.append({"name": name, "imgs": imgs, "encodings": encodings})
 
  f.close()

  with open("encoded.json", "w") as file:
    dump(encoded, file, indent=2)
    file.close()

encode_data()