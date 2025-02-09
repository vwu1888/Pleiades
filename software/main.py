import path_detection
import arduinoBuzz
import cv2
import time

cap = cv2.VideoCapture("/home/vwu/src/Pleiades/videos/oahq1.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    path = path_detection.find_path(frame)
    danger = path_detection.centering(frame, path)
    if danger > 0:
        arduinoBuzz.buzzRight(danger * 100 * 0.5)
    if danger < 0:
        arduinoBuzz.buzzLeft(danger * 100 * 0.5)
    if danger == 0:
        arduinoBuzz.buzzAll(0)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(10/1000)

    

cap.release()
cv2.destroyAllWindows()