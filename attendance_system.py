import cv2
import os
import csv
from datetime import datetime

# Load recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

# Face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

dataset_path = "dataset"
names = os.listdir(dataset_path)

cam = cv2.VideoCapture(0)

def already_marked(name, date):
    if not os.path.exists("attendance.csv"):
        return False
    with open("attendance.csv","r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                if row[0] == name and row[1] == date:
                    return True
    return False

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Improved Liveness: Check for image sharpness/depth
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # If the face is too "flat/blurry" (like a photo), laplacian_var will be low.
        # We use 30 as a safe starting point. 
        if laplacian_var < 30: 
            label = "Spoof Detected"
            color = (0, 0, 255) # Red
        else:
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 65: # Adjusted confidence for better recognition
                name = names[id]
                now = datetime.now()
                date = now.strftime("%d-%m-%Y")
                time = now.strftime("%H:%M:%S")

                if not already_marked(name, date):
                    with open("attendance.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([name, date, time])
                
                label = f"{name}"
                color = (0, 255, 0) # Green
            else:
                label = "Unknown"
                color = (0, 255, 255) # Yellow

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("AI Attendance System", frame)

    if cv2.waitKey(1) == 27: # Press ESC to close
        break

cam.release()
cv2.destroyAllWindows()