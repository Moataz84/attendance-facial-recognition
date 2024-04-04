import cv2
import numpy as np
from json import load
from face_recognition import face_encodings as encode_face, load_image_file, face_locations as get_face_locations, compare_faces, face_distance

known_face_encodings = []
known_face_names = []

f = open("data-1.json")
data = load(f)
for e in data:
  enc = encode_face(load_image_file(f"images/{e['img']}"))
  known_face_encodings.append(enc[0])
  known_face_names.append(e["name"])
f.close()

face_locations = []
face_encodings = []
face_names = []

process_this_frame = True

video_capture = cv2.VideoCapture(0)

while True:
  ret, frame = video_capture.read()

  if process_this_frame:
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
      
    face_locations = get_face_locations(rgb_small_frame)
    face_encodings = encode_face(rgb_small_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
      matches = compare_faces(known_face_encodings, face_encoding)
      name = "Unknown"
      face_distances = face_distance(known_face_encodings, face_encoding)
      best_match_index = np.argmin(face_distances)
      if matches[best_match_index]:
        name = known_face_names[best_match_index]
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