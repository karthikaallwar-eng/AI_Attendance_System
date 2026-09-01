import cv2
import os
import numpy as np
from PIL import Image

dataset_path = "dataset"

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
ids = []
names = {}
current_id = 0

for person_name in os.listdir(dataset_path):

    person_path = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_path):
        continue

    names[current_id] = person_name

    for image_name in os.listdir(person_path):

        image_path = os.path.join(person_path, image_name)

        img = Image.open(image_path).convert('L')

        img_numpy = np.array(img, 'uint8')

        faces.append(img_numpy)
        ids.append(current_id)

    current_id += 1

if not os.path.exists("trainer"):
    os.makedirs("trainer")

recognizer.train(faces, np.array(ids))

recognizer.save("trainer/trainer.yml")

print("Model trained successfully")