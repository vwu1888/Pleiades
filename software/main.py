import path_detection
import buzz_2_a
import cv2
import time

buzz_2_a.pwm_setup()
cap = cv2.VideoCapture("/home/mussel2/Pleiades/videos/oahq1.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    path = path_detection.find_path(frame)
    danger = path_detection.centering(frame, path)
    if danger == 0:
        buzz_2_a.stop_tone(18)
    else:
        buzz_2_a.play_tone(abs(danger)*10, 18)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    

cap.release()
cv2.destroyAllWindows()