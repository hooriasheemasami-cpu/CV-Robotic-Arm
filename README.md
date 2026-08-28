# CV-Robotic-Arm

Computer Vision Robotic Arm

A computer-vision-based robotic arm project using OpenCV for real-time object detection, color identification, coordinate extraction, and pallet-to-box matching. The system initially uses a laptop webcam or mobile phone camera as the visual input.

The current software pipeline focuses on detecting colored objects, extracting their contours and centroids, and converting image pixel coordinates into a coordinate system suitable for robotic manipulation.

The robotic arm control and inverse kinematics components will be integrated at a later stage when the physical hardware becomes available.

## Current Progress

- [x] Camera input
- [x] OpenCV setup
- [x] BGR color representation
- [ ] HSV color segmentation
- [ ] Binary masking
- [ ] Contour detection
- [ ] Image moments
- [ ] Centroid calculation
- [ ] Pixel coordinate extraction
- [ ] Homography transformation
- [ ] Pallet detection
- [ ] Box detection
- [ ] Pallet-to-box matching
- [ ] Real-world coordinate mapping
- [ ] Inverse kinematics
- [ ] Robotic arm control
