from face_recognition import face_encodings, compare_faces, load_image_file
from json import load

f = open("data/encoded.json")
data = load(f)
f.close()

def get_face_data():
  known_face_encodings = []
  known_face_ids = []

  for e in data:
    for encoding in e["encodings"]:
      known_face_encodings.append(encoding)
      known_face_ids.append(e["id"])

  return [known_face_encodings, known_face_ids]

def get_face_result(img_path):
  known_face_encodings, known_face_ids = get_face_data()
  name = "Unknown"
  try:
    query_image = face_encodings(load_image_file(img_path))
    if len(query_image) == 0:
      return "No face detected"
    query_image_encoding = query_image[0]
    result_array = compare_faces(known_face_encodings, query_image_encoding, tolerance=0.4)
    result = result_array.index(True)
    person_id = known_face_ids[result]
    name = list(filter(lambda e: e["id"] == person_id, data))[0]["name"]
    return name
  except:
    return name