import cv2
import numpy as np
from json import load
from face_recognition as load_image_file, face_encodings
import math

known_face_encodings = []
known_face_names = []

f = open("data-1.json")
data = load(f)
for e in data:
  enc = face_encodings(load_image_file(f"images/{e['img']}"))
  known_face_encodings.append(enc[0])
  known_face_names.append(e["name"])
f.close()

face_locations = []
face_encodings = []
face_names = []