import cv2 as cv
import numpy as np
import math

cap = cv.VideoCapture(0)

while(1):
    _, frame = cap.read()

    blurred = cv.GaussianBlur(frame, (5, 5), 0)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

    lower_blue = np.array([90, 80, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    blue = np.uint8([[[255, 0, 0]]])
    hsv_blue = cv.cvtColor(blue, cv.COLOR_BGR2HSV) 
    print(hsv_blue)

    lower_green = np.array([35, 80, 50])
    upper_green = np.array([85, 255, 255])
    mask2 = cv.inRange(hsv, lower_green, upper_green)

    green = np.uint8([[[0, 255, 0]]])
    hsv_green = cv.cvtColor(green, cv.COLOR_BGR2HSV)
    print(hsv_green)

    lower_red = np.array([0, 80, 50])
    upper_red = np.array([10, 255, 255])
    mask3 = cv.inRange(hsv, lower_red, upper_red)

    red = np.uint8([[[0, 0, 255]]])
    hsv_red = cv.cvtColor(red, cv.COLOR_BGR2HSV)
    print(hsv_red)

    b_g_mask = cv.bitwise_or(mask, mask2)
    final_mask = cv.bitwise_or(b_g_mask, mask3)
    mask_bgr = cv.cvtColor(final_mask, cv.COLOR_GRAY2BGR)
    result = cv.bitwise_and(frame, frame, mask=final_mask)

    kernel = np.ones((5, 5), np.uint8)
    final_mask = cv.morphologyEx(final_mask, cv.MORPH_OPEN, kernel)
    final_mask = cv.morphologyEx(final_mask, cv.MORPH_CLOSE, kernel)

    contours, heirarchy = cv.findContours(
        final_mask,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        area = cv.contourArea(contour)
        if area > 500:
            M = cv.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                print("Centroid: ", cx, cy)                
                cv.drawContours(frame, contours, -1, (0, 255, 0), 3)
                cv.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
                

    def detect_objects(mask, color_name):
        red_objects = detect_objects(mask3, "Red")
        green_objects = detect_objects(mask2, "Green")
        blue_objects = detect_objects(mask, "Blue")

    # change the image points and world points based on calibration

    image_points = np.float32([
        [100, 100],  # Top-left corner
        [500, 100],  # Top-right corner
        [500, 400],  # Bottom-right corner
        [100, 400]   # Bottom-left corner
    ])

    world_points = np.float32([
        [0, 0],      # Corresponding world coordinates for top-left corner
        [50, 0],      # Corresponding world coordinates for top-right corner
        [50, 50],      # Corresponding world coordinates for bottom-right corner
        [0, 50]       # Corresponding world coordinates for bottom-left corner
    ])

    H, _ = cv.findHomography(image_points, world_points)

    def pixel_to_world(cx, cy):
                pixel_point = np.array([[cx], [cy], [1]], dtype=np.float32)
                world_point = np.dot(H, pixel_point)
                world_point /= world_point[2]
                X = world_point[0][0]
                Y = world_point[1][0]
                Z = 0  # Assuming Z=0 for a flat surface
                return X, Y, Z

    key = cv.waitKey(5) & 0xFF

    if key == ord('s'):
        cv.imwrite("image.jpg", frame)
        print("Image saved as image.jpg")

    if key == ord('p'):
        break

    cv.imshow("frame", frame)
    cv.imshow("final_mask", final_mask)
    cv.imshow("result", result)

cap.release()
cv.destroyAllWindows()
cv.waitKey(5)

# testing the homography function

test_X, test_Y, test_Z = pixel_to_world(250, 250)
print(f"Test position: X={test_X} cm, Y={test_Y} cm, Z={test_Z} cm")

# testing the corners

print(pixel_to_world(100, 100))
print(pixel_to_world(500, 100))
print(pixel_to_world(500, 400))
print(pixel_to_world(100, 400))
