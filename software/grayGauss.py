import numpy as np
import cv2
import imutils

color = (255, 255, 255)
colors = {'blue': [np.array([150, 70, 0]), np.array([200, 110, 40])],}

cap = cv2.VideoCapture("/home/vwu/src/Pleiades/videos/oahq1.mp4")

if not cap.isOpened():
    print("Cannot open camera")
    exit()


def find_color(frame, points):
    mask = cv2.inRange(frame, points[0], points[1])  # create mask with boundaries
    cv2.imshow('mask', mask)
    cnts = cv2.findContours(mask, cv2.RETR_TREE,
                           cv2.CHAIN_APPROX_SIMPLE)  # find contours from mask
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        area = cv2.contourArea(c)  # find how big countour is
        if area > 5000:  # only if countour is big enough, then
            M = cv2.moments(c)
            cx = int(M['m10'] / M['m00'])  # calculate X position
            cy = int(M['m01'] / M['m00'])  # calculate Y position
            return c, cx, cy


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[700:frame.shape[0], 0:frame.shape[1]]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGRA2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 75, 175, 3)
    lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 150, 0, 100, 100)

    if lines is not None:
        for l in lines:
            for x1, y1, x2, y2 in l:
                if x2 == x1:
                    continue
                if abs((y2 - y1) / (x2 - x1)) > 1:
                    cv2.line(frame, (x1, y1+700), (x2, y2+700), (255, 255, 255), 10, 5)

    cv2.imshow('canny', canny)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

def convert():
    print()