from face_recognition import face_encodings, compare_faces, load_image_file
from json import load, dump

def get_face_data():
  f = open("data/encoded.json")
  data = load(f)
  f.close()

  known_face_encodings = []
  known_face_ids = []

  for e in data:
    for encoding in e["encodings"]:
      known_face_encodings.append(encoding)
      known_face_ids.append(e["id"])

  return [known_face_encodings, known_face_ids, data]

def append_encoding(e, id, encoding):
  if e["id"] == id:
    if len(e["encodings"]) <= 200:
      return {
        "id": e["id"], 
        "name": e["name"], 
        "encodings": e["encodings"] + [encoding.tolist()]
      }
    return {
      "id": e["id"], 
      "name": e["name"], 
      "encodings": e["encodings"][1:] + [encoding.tolist()]
    }
  return e

def append_face_data(id, encoding, data):
  new_encodings = list(map(lambda e: append_encoding(e, id, encoding), data))
  with open("data/encoded.json", "w") as file:
    dump(new_encodings, file, indent=2)
    file.close() 

def get_face_result(img_path):
  known_face_encodings, known_face_ids, data = get_face_data()
  person_id = None
  try:
    query_image = face_encodings(load_image_file(img_path))
    if len(query_image) == 0:
      return [person_id, "No face detected"]
    query_image_encoding = query_image[0]
    result_array = compare_faces(known_face_encodings, query_image_encoding, tolerance=0.4)
    result = result_array.index(True)
    person_id = known_face_ids[result]
    append_face_data(person_id, query_image_encoding, data)
    name = list(filter(lambda e: e["id"] == person_id, data))[0]["name"]
    return [person_id, name]
  except:
    return [person_id, "Unknown person"]