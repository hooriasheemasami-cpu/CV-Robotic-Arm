import cv2 as cv
import numpy as np
import math

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

pallets = {
    "Red": [0, 0, 0],
    "Green": [0, 0, 0],
    "Blue": [0, 0, 0]
}

def get_color_world_pos(hsv_frame, lower_color, upper_color):
    final_mask = cv.inRange(hsv_frame, lower_color, upper_color)

    # perform morphological operations to clean up the mask
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

                return pixel_to_world(cx, cy)
    return None

def inverse_kinematics(x, y, z, L1, L2):
    theta1 = math.atan2(y, x)
    r = math.sqrt(x**2 + y**2)
    d = math.sqrt(r**2 + z**2)
    if d > (L1 + L2) or d < abs(L1 - L2):
        return None  # Target is unreachable

    cos_theta2 = (
        r**2 + z**2 - L1**2 - L2**2
    ) / (2 * L1 * L2)

    cos_theta2 = max(-1, min(1, cos_theta2))
    theta2 = math.acos(cos_theta2)
    alpha = math.atan2(z, r)
    beta = math.atan2(
        L2 * math.sin(theta2),
        L1 + L2 * math.cos(theta2)
    )

    theta3 = alpha - beta

    return (
        math.degrees(theta1),
        math.degrees(theta2),
        math.degrees(theta3)
    )
    
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
                
    # perform morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    final_mask = cv.morphologyEx(final_mask, cv.MORPH_OPEN, kernel)
    final_mask = cv.morphologyEx(final_mask, cv.MORPH_CLOSE, kernel)

    contours, heirarchy = cv.findContours(
        final_mask,
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )

    boxes = {
        "Red": None,
        "Green": None,
        "Blue": None
    }

    for contour in contours:
        area = cv.contourArea(contour)
        if area > 500:
            M = cv.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                print("Centroid:", cx, cy)
                cv.drawContours(frame, [contour], -1, (0, 255, 0), 3)
                cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

                # Determine the color of the object based on the mask
                if mask3[cy, cx] > 0:
                    color_name = "Red"
                elif mask2[cy, cx] > 0:
                    color_name = "Green"
                elif mask[cy, cx] > 0:
                    color_name = "Blue"

                if color_name is not None:
                    # Convert the pixel coordinates to world coordinates
                    X, Y, Z = pixel_to_world(cx, cy)
                    boxes[color_name] = (X, Y, Z)

    tasks = []
    for color in boxes:
        if boxes[color] is not None and pallets.get(color) is not None:
            tasks.append({
                "color": color,
                "pick": boxes[color],
                "place": pallets[color]
            })

    if tasks:
        print("Tasks:")
        for task in tasks:
            pick_x, pick_y, pick_z = task["pick"]
            pick_angles = inverse_kinematics(
                pick_x,
                pick_y,
                pick_z,
                L1 = 10,
                L2 = 10
            )

            print(f"Pick {task['color']} at {task['pick']}: Angles = {pick_angles}")
            print(f"Place at {task['place']}")

    key = cv.waitKey(5) & 0xFF

    if key == ord('p'):
        break

    cv.imshow("frame", frame)
    cv.imshow("final_mask", final_mask)
    cv.imshow("result", result)

cap.release()
cv.destroyAllWindows()
cv.waitKey(5)

# testing the homography function

# test_X, test_Y, test_Z = pixel_to_world(300, 250)
# print(f"World coordinates for pixel (300, 250): X={test_X}, Y={test_Y}, Z={test_Z}")

# testing the corners

# print(pixel_to_world(100, 100))
# print(pixel_to_world(500, 100))
# print(pixel_to_world(500, 400))
# print(pixel_to_world(100, 400))
