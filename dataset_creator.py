import cv2
import os

cam = cv2.VideoCapture(0)

name = input("Enter student name: ")

path = "dataset/" + name

if not os.path.exists(path):
    os.makedirs(path)

count = 0

while True:
    ret, frame = cam.read()

    if not ret:
        print("Camera error")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        count += 1

        face = gray[y:y+h, x:x+w]

        cv2.imwrite(path + "/" + str(count) + ".jpg", face)

        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    cv2.imshow("Face Capture", frame)

    if count >= 50:
        break

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()