import path_detection
import Person_Detection
import arduinoBuzz
import cv2
import time

cap = cv2.VideoCapture("/home/vwu/src/Pleiades/videos/oahq1.mp4")
# cap = cv2.VideoCapture(0)

def pathCorrection(danger):
    if danger > 0:
        arduinoBuzz.buzzRight(danger * 100 * 0.5)
    if danger < 0:
        arduinoBuzz.buzzLeft(danger * 100 * 0.5)
    if danger == 0:
        arduinoBuzz.buzzAll(0)

def collisionAvoidance(danger):
    if danger == 0:
        arduinoBuzz.buzzAll(0)
    elif abs(danger) < 10:
        arduinoBuzz.buzzAll(3000)
    elif danger < 40:
        arduinoBuzz.buzzRight(5 // danger * 100)
    elif danger > -40:
        arduinoBuzz.buzzLeft(50 // danger * 100)


while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    path = path_detection.find_path(gray)
    offPath = path_detection.centering(frame, path)
    pathCorrection(offPath)

    faces = Person_Detection.person_detection(gray)
    collisionProb = Person_Detection.person_danger(frame, faces)
    collisionAvoidance(collisionProb)

    path_detection.draw(frame, path)
    Person_Detection.draw(frame, faces)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(10/1000)

    

cap.release()
cv2.destroyAllWindows()