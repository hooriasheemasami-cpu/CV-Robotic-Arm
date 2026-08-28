# CV-Robotic-Arm

Computer Vision Robotic Arm

A computer-vision-based robotic arm project using OpenCV for real-time object detection, color identification, coordinate extraction, and pallet-to-box matching. The system initially uses a laptop webcam or mobile phone camera as the visual input.

The current software pipeline focuses on detecting colored objects, extracting their contours and centroids, and converting image pixel coordinates into a coordinate system suitable for robotic manipulation.

The robotic arm control and inverse kinematics components will be integrated at a later stage when the physical hardware becomes available.

## Current Progress

- [x] Camera input
- [x] OpenCV setup
- [x] BGR color representation
- [x] HSV color segmentation
- [x] Binary masking
- [x] Contour detection
- [x] Image moments
- [x] Centroid calculation
- [ ] Pixel coordinate extraction
- [ ] Homography transformation
- [ ] Pallet detection
- [ ] Box detection
- [ ] Pallet-to-box matching
- [ ] Real-world coordinate mapping
- [ ] Inverse kinematics
- [ ] Robotic arm control

## Hardware Status

The computer-vision component is being developed without the physical robotic arm. A laptop webcam or mobile phone camera is used for visual input and software testing.

Inverse kinematics and robotic-arm control will be implemented once the physical hardware is available.
