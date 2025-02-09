import cv2

borderOffset = 125
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

if face_cascade.empty():
    print("Error loading Haar cascade classifier!")

def person_danger(frame, faces):
    xCenter = frame.shape[1] / 2

    for (x, y, w, h) in faces:
        xFace = x + w / 2

        dXFace = xCenter - xFace
        if abs(dXFace) < 100:
            cv2.putText(frame, "Collision Imminent!", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return dXFace

    return 0

def draw(frame, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

def person_detection(frame):
    roi = frame[borderOffset:frame.shape[0] - borderOffset, borderOffset:frame.shape[1] - borderOffset]
    faces = face_cascade.detectMultiScale(roi, scaleFactor=1.1, minNeighbors=3, minSize=(45, 45))
    for face in faces:
        face[0] += borderOffset
        face[1] += borderOffset

    return faces