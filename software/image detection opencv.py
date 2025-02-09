import numpy as np
import pandas as pd
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip



def region_selection(image):
    """
	Determine and cut the region of interest in the input image.
	Parameters:
		image: we pass here the output from canny where we have
		identified edges in the frame
	"""
    mask = np.zeros_like(image)
    if len(image.shape) > 2:
        channel_count = image.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    rows, cols = image.shape[:2]
    bottom_left = [cols * 0.01, rows * 0.98]
    top_left = [cols * 0.25, rows * 0.5]
    bottom_right = [cols * 0.99, rows * 0.98]
    top_right = [cols * 0.75, rows * 0.5]
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)

    cv2.fillPoly(mask, vertices, ignore_mask_color)

    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def hough_transform(image):

    rho = 1
    theta = np.pi / 180
    threshold = 40
    minLineLength = 40
    maxLineGap = 500

    lines = cv2.HoughLinesP(image, rho, theta, threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)

    if lines is None:
        return []
    filtered_lines = []
    slopes = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                continue
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) < .3:
                continue

            if all(abs(slope - s) > 0.1 for s in slopes):
                filtered_lines.append(line)
                slopes.append(slope)

    return filtered_lines


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


def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=15):
    line_image = np.zeros_like(image)
    drawn_lines = set()
    for line in lines:
        if line is not None and isinstance(line, tuple):
            if line not in drawn_lines:
                cv2.line(line_image, *line, color, thickness)
                drawn_lines.add(line)
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)


def frame_processor(image):
    image = image.copy()
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel_size = 5
    blur = cv2.GaussianBlur(grayscale, (kernel_size, kernel_size), 0)
    low_t = 40
    high_t = 100
    edges = cv2.Canny(blur, low_t, high_t)
    region = region_selection(edges)
    hough = hough_transform(region)
    if len(hough) == 0 or len(lane_lines(image, hough)) < 2:
        return image

    lanes = lane_lines(image, hough)
    mid_x = image.shape[1] // 2  # Get frame center
    left_x = lanes[0][0][0] if len(lanes) > 0 else None
    right_x = lanes[1][0][0] if len(lanes) > 1 else None

    if left_x is not None and right_x is not None:
        center_offset = (left_x + right_x) // 2 - mid_x
        if abs(center_offset) > 150:

            cv2.putText(image, "Approaching Edge!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    result = draw_lane_lines(image, lane_lines(image, hough))
    return result


def process_video(test_video, output_video):
    input_video = VideoFileClip(test_video, audio=False)
    processed = input_video.transform(lambda gf, t: frame_processor(gf(t)))
    processed.write_videofile(output_video, codec="libx264", audio=False)

# calling driver function
process_video("/Users/noah/Desktop/python project/Pleiades/videos/SAD1.mp4", "/Users/noah/Desktop/python project/Pleiades/videos/output.mp4")