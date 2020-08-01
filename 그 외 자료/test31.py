## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2

## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2

pipeline = rs.pipeline()

config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

profile = pipeline.start(config)

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

clipping_distance_in_meters = 1 
clipping_distance = clipping_distance_in_meters / depth_scale

align_to = rs.stream.color
align = rs.align(align_to)

frames = pipeline.wait_for_frames()
aligned_frames = align.process(frames)

aligned_depth_frame = aligned_frames.get_depth_frame() 
color_frame = aligned_frames.get_color_frame()

depth_image = np.asanyarray(aligned_depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())

test = cv2.cvtColor(color_image, cv2.COLOR_BGR2YCrCb)

grey_color = 153        
depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) 
bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
mask_hand = cv2.inRange(test, np.array([0,133,77]),np.array([255,173,127])) # 살색 > 흰색, 나머지 > 검은색

depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)        
images = np.hstack((color_image, bg_removed, depth_colormap))
#cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Align Example1', color_image)
cv2.imshow('Align Example2', bg_removed)
cv2.imshow('Align Example3', depth_colormap)
cv2.imshow('Align Example4', mask_hand)
cv2.waitKey(1)

img_gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
ret, img_binary = cv2.threshold(img_gray, 127, 255, 0)
contours, hierarchty = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    cv2.drawContours(color_image, [cnt], 0, (255,0,0), 3)

cv2.imshow("result", color_image)
cv2.waitKey(0)

for cnt in contours:
    hull = cv2.convexHull(cnt)
    cv2.drawContours(color_image, [hull], 0, (255,0,255), 5)

cv2.imshow("result2", color_image)
cv2.waitKey(0)

pipeline.stop()

'''
# Streaming loop
try:
    while True:
        
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        aligned_depth_frame = aligned_frames.get_depth_frame() 
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        test = cv2.cvtColor(color_image, cv2.COLOR_BGR2YCrCb)

        grey_color = 153        
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) 
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
        mask_hand = cv2.inRange(test, np.array([0,133,77]),np.array([255,173,127])) # 살색 > 흰색, 나머지 > 검은색

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)        
        images = np.hstack((color_image, bg_removed, depth_colormap))
        #cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Align Example1', color_image)
        cv2.imshow('Align Example2', bg_removed)
        cv2.imshow('Align Example3', depth_colormap)
        cv2.imshow('Align Example4', mask_hand)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
                
finally:
    pipeline.stop()
'''

'''
pipeline = rs.pipeline()
pipe = rs.pipeline()

config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

profile = pipeline.start(config)
pipe.start(cfg)

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

clipping_distance_in_meters = 1 
clipping_distance = clipping_distance_in_meters / depth_scale

align_to = rs.stream.color
align = rs.align(align_to)

# Streaming loop
try:
    while True:
        
        tframe = pipe.wait_for_frames()
        pose = tframe.get_pose_frame()
        
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        aligned_depth_frame = aligned_frames.get_depth_frame() 
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) 
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        #images = np.hstack((color_image, bg_removed, depth_colormap))
        cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Align Example', bg_removed)
        key = cv2.waitKey(1)

        if pose:
            data = pose.get_pose_data()
            print("Frame #{}".format(pose.frame_number))
            print("Position: {}".format(data.translation))
            print("Velocity: {}".format(data.velocity))
            print("Acceleration: {}\n".format(data.acceleration))

        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
                
finally:
    pipeline.stop()
'''
