#!/usr/bin/python
# -*- coding: utf-8 -*-
## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2019 Intel Corporation. All Rights Reserved.
# Python 2/3 compatibility
from __future__ import print_function

# import the library
import os
import cv2
import time
import pandas as pd
import numpy as np
import tkinter as tk
import pyrealsense2 as rs
import matplotlib.pyplot as plt
from tkinter import *
from math import tan, pi
from threading import Lock

frame_mutex = Lock()
frame_data = { "left"  : None,
                     "right" : None,
                     "timestamp_ms" : None }

def get_extrinsics(src, dst):
    extrinsics = src.get_extrinsics_to(dst)
    R = np.reshape(extrinsics.rotation, [3,3]).T
    T = np.array(extrinsics.translation)
    return (R, T)

def camera_matrix(intrinsics):
    return np.array([[intrinsics.fx, 0,                intrinsics.ppx],
                           [0,                intrinsics.fy, intrinsics.ppy],
                           [0,                0,                1]])

def fisheye_distortion(intrinsics):
    return np.array(intrinsics.coeffs[:4])

def callback(frame):
    global frame_data
    if frame.is_frameset():
        frameset = frame.as_frameset()
        f1 = frameset.get_fisheye_frame(1).as_video_frame()
        f2 = frameset.get_fisheye_frame(2).as_video_frame()
        left_data = np.asanyarray(f1.get_data())
        right_data = np.asanyarray(f2.get_data())
        ts = frameset.get_timestamp()
        frame_mutex.acquire()
        frame_data["left"] = left_data
        frame_data["right"] = right_data
        frame_data["timestamp_ms"] = ts
        frame_mutex.release()
        
pipe = rs.pipeline()
cfg = rs.config()
pipe.start(cfg, callback)

try:
    WINDOW_TITLE = 'Realsense'
    cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)

    window_size = 5
    min_disp = 0

    num_disp = 112 - min_disp
    max_disp = min_disp + num_disp
    stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
                                                    numDisparities = num_disp,
                                                    blockSize = 16,
                                                    P1 = 8*3*window_size**2,
                                                    P2 = 32*3*window_size**2,
                                                    disp12MaxDiff = 1,
                                                    uniquenessRatio = 10,
                                                    speckleWindowSize = 100,
                                                    speckleRange = 32)

    profiles = pipe.get_active_profile()
    streams   = {"left"  : profiles.get_stream(rs.stream.fisheye, 1).as_video_stream_profile(),
                      "right" : profiles.get_stream(rs.stream.fisheye, 2).as_video_stream_profile()}
    intrinsics = {"left"  : streams["left"].get_intrinsics(),
                      "right" : streams["right"].get_intrinsics()}
    
    print("Left camera:",  intrinsics["left"])
    print("Right camera:", intrinsics["right"])

    K_left  = camera_matrix(intrinsics["left"])
    D_left  = fisheye_distortion(intrinsics["left"])
    K_right = camera_matrix(intrinsics["right"])
    D_right = fisheye_distortion(intrinsics["right"])
    (width, height) = (intrinsics["left"].width, intrinsics["left"].height)

    (R, T) = get_extrinsics(streams["left"], streams["right"])

    stereo_fov_rad = 90 * (pi/180) 
    stereo_height_px = 300      
    stereo_focal_px = stereo_height_px/2 / tan(stereo_fov_rad/2)

    R_left = np.eye(3)
    R_right = R

    stereo_width_px = stereo_height_px + max_disp
    stereo_size = (stereo_width_px, stereo_height_px)
    stereo_cx = (stereo_height_px - 1)/2 + max_disp
    stereo_cy = (stereo_height_px - 1)/2

    P_left = np.array([[stereo_focal_px,    0,                          stereo_cx,        0],
                             [0,                        stereo_focal_px,      stereo_cy,        0],
                             [0,                        0,                          1,                    0]])
    P_right = P_left.copy()
    P_right[0][3] = T[0]*stereo_focal_px

    Q = np.array([[1,       0,            0,          -(stereo_cx - max_disp)],
                        [0,       1,            0,          -stereo_cy],
                        [0,       0,            0,          stereo_focal_px],
                        [0,       0,    -1/T[0],         0]])

    m1type = cv2.CV_32FC1
    (lm1, lm2) = cv2.fisheye.initUndistortRectifyMap(K_left, D_left, R_left, P_left, stereo_size, m1type)
    (rm1, rm2) = cv2.fisheye.initUndistortRectifyMap(K_right, D_right, R_right, P_right, stereo_size, m1type)
    undistort_rectify = {"left"  : (lm1, lm2), "right" : (rm1, rm2)}

    
    while True:      
            
        frame_mutex.acquire()
        valid = frame_data["timestamp_ms"] is not None
        frame_mutex.release()
        
        if valid:
            frame_mutex.acquire()
            frame_copy = {"left"  : frame_data["left"].copy(),
                                "right" : frame_data["right"].copy()}
            frame_mutex.release()

            center_undistorted = {"left" : cv2.remap(src = frame_copy["left"],
                                           map1 = undistort_rectify["left"][0],
                                           map2 = undistort_rectify["left"][1],
                                           interpolation = cv2.INTER_LINEAR),
                                  
                                          "right" : cv2.remap(src = frame_copy["right"],
                                           map1 = undistort_rectify["right"][0],
                                           map2 = undistort_rectify["right"][1],
                                           interpolation = cv2.INTER_LINEAR)}
            
            color_image = cv2.cvtColor(center_undistorted["left"][:,max_disp:], cv2.COLOR_GRAY2RGB)            
            cv2.imshow(WINDOW_TITLE, color_image)

        key = cv2.waitKey(1)        
        if key == ord('q') or cv2.getWindowProperty(WINDOW_TITLE, cv2.WND_PROP_VISIBLE) < 1:  # 창닫기
            break
finally:
    pipe.stop()



























