from face_recognition import face_encodings as encode_face, face_locations as get_face_locations, compare_faces, face_distance
from numpy import ascontiguousarray, argmin
from json import load
import cv2

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

known_face_encodings, known_face_ids = get_face_data()

face_locations = []
face_encodings = []
face_names = []

process_this_frame = True

video_capture = cv2.VideoCapture(0)

while True:
  ret, frame = video_capture.read()

  if process_this_frame:
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = ascontiguousarray(small_frame[:, :, ::-1])
      
    face_locations = get_face_locations(rgb_small_frame)
    face_encodings = encode_face(rgb_small_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
      matches = compare_faces(known_face_encodings, face_encoding)
      name = "Unknown"
      face_distances = face_distance(known_face_encodings, face_encoding)
      best_match_index = argmin(face_distances)
      if matches[best_match_index]:
        id = known_face_ids[best_match_index]
        name = list(filter(lambda e: e["id"] == id, data))[0]["name"]
      face_names.append(name)

  process_this_frame = not process_this_frame

  for (top, right, bottom, left), name in zip(face_locations, face_names):
    top *= 4
    right *= 4
    bottom *= 4
    left *= 4
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

  cv2.imshow("Video", frame)

  if cv2.waitKey(1) & 0xFF == ord("q"):
    break

video_capture.release()
cv2.destroyAllWindows()