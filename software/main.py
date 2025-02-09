import path_detection
import Person_Detection
import arduinoBuzz
import cv2
import time

cap = cv2.VideoCapture("/home/vwu/src/Pleiades/videos/path.mp4")

def pathCorrection(danger):
    if danger > 0:
        arduinoBuzz.buzzRight(danger * 10)
    if danger < 0:
        arduinoBuzz.buzzLeft(danger * 10)
    if danger == 0:
        arduinoBuzz.buzzAll(0)

def collisionAvoidance(danger):
    if danger == 0 or abs(danger) >= 80:
        arduinoBuzz.buzzAll(0)
        collisionWarning = False
    elif abs(danger) < 30:
        arduinoBuzz.buzzAll(5000)
        collisionWarning = True
    elif danger < 80:
        arduinoBuzz.buzzRight(5 // danger * 4000)
        collisionWarning = True
    elif danger > -80:
        arduinoBuzz.buzzLeft(5 // danger * 4000)
        collisionWarning = True



while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    path = path_detection.find_path(gray)
    offPath = path_detection.centering(frame, path)

    faces = Person_Detection.person_detection(gray)
    collisionProb = Person_Detection.person_danger(frame, faces)

    pathCorrection(offPath)
    collisionAvoidance(collisionProb)

    path_detection.draw(frame, path)
    Person_Detection.draw(frame, faces)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(10/1000)

    

cap.release()
cv2.destroyAllWindows()