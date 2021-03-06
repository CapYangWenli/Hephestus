import cv2
import numpy as np
import logging
import math
import datetime
import sys


def detect_lane(frame, hsv, lower_blue, upper_blue, mask, edges):
 
    # edges = detect_edges(frame)

    cropped_edges = region_of_interest(edges)
    
    line_segments = detect_line_segments(cropped_edges)
    line_segment_image = display_lines(frame, line_segments)
    # cv2.imshow("line segments", line_segment_image)
    
    lane_lines = average_slope_intercept(frame, line_segments)

    steering_angle = compute_steering_angle(frame, lane_lines)
    
    final_image = display_final_lines(frame, steering_angle, lane_lines)
    # cv2.imshow("heading_image", final_image)
    
    return lane_lines, steering_angle

def detect_edges(frame):
    # filter for blue lane lines
    
    # detect edges
    return edges


def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    # only focus bottom half of the screen
    polygon = np.array([[
        (0, height * 2 / 3),
        (width, height * 2 / 3),
        (width, height * 5 /6),
        (0, height * 5 / 6),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)
    return cropped_edges


def detect_line_segments(cropped_edges):
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, np.array([]), minLineLength=8, maxLineGap=4)
    return line_segments

def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        logging.info('No line_segment segments detected')
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                logging.info('skipping vertical line segment (slope=inf): %s' % line_segment)
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    logging.debug('lane lines: %s' % lane_lines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]

    return lane_lines

def compute_steering_angle(frame, lane_lines):
    """ Find the steering angle based on lane line coordinate
        We assume that camera is calibrated to point to dead center
    """
    if len(lane_lines) == 0:
        logging.info('No lane lines detected, do nothing')
        return -90

    height, width, _ = frame.shape
    if len(lane_lines) == 1:
        logging.debug('Only detected one lane line, just follow it. %s' % lane_lines[0])
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        camera_mid_offset_percent = 0.02 # 0.0 means car pointing to center, -0.03: car is centered to left, +0.03 means car pointing to right
        mid = int(width / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid

    # find the steering angle, which is angle between navigation direction to end of center line
    y_offset = int(height / 2)

    angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
    steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed by picar front wheel
    logging.debug('new steering angle: %s' % steering_angle)
    return steering_angle

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


def display_final_lines(frame, steering_angle, lines, line_color=(0, 255, 0), line_width=2):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape
    

    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_image, (x1, y1), (x2, y2), (0, 0, 255), line_width)
    line_image = cv2.addWeighted(line_image, 1, heading_image, 1, 1)
    
    return line_image


def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5 ):
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape
    # figure out the heading line from steering angle
    # heading line (x1,y1) is always center bottom of the screen
    # (x2, y2) requires a bit of trigonometry

    # Note: the steering angle of:
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right 
    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)
    return heading_image


def make_points(frame, line):
        height, width, _ = frame.shape
        slope, intercept = line
        y1 = height  # bottom of the frame
        y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

        # bound the coordinates within the frame
        x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
        x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
        return [[x1, y1, x2, y2]]

def nothing():
    pass

def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("track", cv2.WINDOW_NORMAL)
 
    cv2.createTrackbar ("HL","track", 0, 180, nothing)
    cv2.createTrackbar ("SL","track", 0, 255, nothing)
    cv2.createTrackbar ("VL","track", 0, 255, nothing)
    
    cv2.createTrackbar ("H","track", 0, 180, nothing)
    cv2.createTrackbar ("S","track", 0, 255, nothing)
    cv2.createTrackbar ("V","track", 0, 255, nothing)

    while True:

        hl = cv2.getTrackbarPos ("HL","track")
        sl = cv2.getTrackbarPos ("SL", "track")
        vl = cv2.getTrackbarPos ("VL", "track")
        
        h = cv2.getTrackbarPos ("H","track")
        s = cv2.getTrackbarPos ("S", "track")
        v = cv2.getTrackbarPos ("V", "track")

        lower_blue = np.array([hl, sl, vl])
        upper_blue = np.array([h, s, v])

        print(lower_blue)
        print(upper_blue)

        ret, frame = cap.read()
        # cv2.imshow("video", frame) 



        kernel = np.ones((5, 5), np.uint8)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # cv2.imshow("HSV", hsv)
        cv2.imshow("Mask", mask)

        # grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # grey_edges = cv2.Canny(grey, 200, 400)

        # image = cv2.bitwise_and(grey_edges, mask)
        # cv2.imshow("Grey edges + Mask", image)

        edges = cv2.Canny(mask, 200, 400)
        cv2.imshow("HSV Edges", edges)
        # cv2.imshow("Grey Edges", grey_edges)
        cropped_edges = cv2.bitwise_and(edges, mask)
        detect_lane(frame, hsv, lower_blue, upper_blue, mask, edges)
        if cv2.waitKey(1)&0xFF == ord("q"):
            break
    cap.release()

if __name__ == '__main__':
    main()

cv2.destroyAllWindows()  

   



   





