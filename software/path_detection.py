import numpy as np
import cv2

yOffset = 700
def average_slope_intercept(lines):

    left_lines = []
    left_weights = []
    right_lines = []
    right_weights = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                continue
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)
            length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
            if slope < 0:
                left_lines.append((slope, intercept))
                left_weights.append((length))
            else:
                right_lines.append((slope, intercept))
                right_weights.append((length))
    #
    left_lane = np.dot(left_weights, left_lines) / np.sum(left_weights) if len(left_weights) > 0 else None
    right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
    return left_lane, right_lane
def pixel_points(y1, y2, line):
    if line is None:
        return None
    slope, intercept = line
    if abs(slope) > 1000 or slope == 0:
        return None

    try:
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
    except (OverflowError, ValueError):
        return None

    return ((x1, y1), (x2, y2))


def lane_lines(image, lines):
    left_lane, right_lane = average_slope_intercept(lines)
    y1 = image.shape[0]
    y2 = int(y1 * 0.6)
    left_line = pixel_points(y1, y2, left_lane)
    right_line = pixel_points(y1, y2, right_lane)
    return list(set([line for line in [left_line, right_line] if line is not None]))

def centering(image, lines):
    lanes = lane_lines(image, lines)
    mid_x = image.shape[1] // 2  # Get frame center
    left_x = lanes[0][0][0] if len(lanes) > 0 else None
    right_x = lanes[1][0][0] if len(lanes) > 1 else None

    if left_x is not None and right_x is not None:
        center_offset = (left_x + right_x) // 2 - mid_x
        if abs(center_offset) > 150:
            cv2.putText(image, "Approaching Edge!", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return center_offset
    return 0

def find_path(frame):
    path = []

    roi = frame[yOffset:frame.shape[0], 0:frame.shape[1]]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGRA2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 75, 175, 3)
    cv2.imshow("Canny", canny)
    lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 150, 0, 100, 100)

    if lines is not None:
        for l in lines:
            for x1, y1, x2, y2 in l:
                if x2 == x1:
                    continue
                if abs((y2 - y1) / (x2 - x1)) > 1:
                    cv2.line(frame, (x1, y1+yOffset), (x2, y2+yOffset), (255, 255, 255), 10, 5)
                    path.append(l)

    return path