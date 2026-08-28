import cv2 as cv
import numpy as np

url = "http://192.168.0.103:4747/video"
cap = cv.VideoCapture(url)
print("Camera is opened: ", cap.isOpened())

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv.imshow("Camera Feed", frame)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break

while(1):
    _, frame = cap.read()

    blurred = cv.GaussianBlur(frame, (5, 5), 0)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    blue = np.uint8([[[255, 0, 0]]])
    hsv_blue = cv.cvtColor(blue, cv.COLOR_BGR2HSV) 
    print(hsv_blue)

    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])
    mask2 = cv.inRange(hsv, lower_green, upper_green)

    green = np.uint8([[[0, 255, 0]]])
    hsv_green = cv.cvtColor(green, cv.COLOR_BGR2HSV)
    print(hsv_green)

    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask3 = cv.inRange(hsv, lower_red, upper_red)

    red = np.uint8([[[0, 0, 255]]])
    hsv_red = cv.cvtColor(red, cv.COLOR_BGR2HSV)
    print(hsv_red)

    b_g_mask = cv.bitwise_or(mask, mask2)
    final_mask = cv.bitwise_or(b_g_mask, mask3)
    mask_bgr = cv.cvtColor(final_mask, cv.COLOR_GRAY2BGR)
    result = cv.bitwise_and(frame, frame, mask=final_mask)

    contours, heirarchy = cv.findContours(
        mask,
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
