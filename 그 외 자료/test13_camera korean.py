#!/usr/bin/python
# -*- coding: utf-8 -*-
## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2019 Intel Corporation. All Rights Reserved.
# Python 2/3 compatibility
from __future__ import print_function

"""
이 예는 호스트의 T265 fisheye 영상에서 깊이 맵을 비동기적으로 계산하기 위해 OpenCV에서 T265 본질과 외연을 사용하는 방법을 보여준다.
T265는 깊이 카메라가 아니며 패시브 전용 깊이 옵션의 품질은 D4XX 시리즈 카메라와 비교했을 때 항상 제한된다.
그러나 T265에는 스테레오 구성의 두 개의 글로벌 셔터 카메라가 있으며,
이 예에서는 OpenCV를 설정하여 이미지를 분리하고 스테레오 깊이를 계산하는 방법을 보여준다.
Ubuntu 16.04에서 python3, OpenCV 및 T265 시작:
먼저 가상 환경 설정:
$ apt-get install python3-venv  # install python3 built in venv support
$ python3 -m venv py3librs      # create a virtual environment in pylibrs
$ source py3librs/bin/activate  # activate the venv, do this from every terminal
$ pip install opencv-python     # install opencv 4.1 in the venv
$ pip install pyrealsense2      # install librealsense python bindings
Then, for every new terminal:
$ source py3librs/bin/activate  # Activate the virtual environment
$ python3 t265_stereo.py        # Run the example
"""

# import the library
import pyrealsense2 as rs
import cv2
import numpy as np
from math import tan, pi

"""
이 섹션에서는 카메라의 본질과 외부를 librealsense에서 OpenCV와 함께 사용할 수 있는 파라미터로 변환하는 기능을 설정하겠다.
T265는 매우 넓은 앵글 렌즈를 사용하기 때문에 왜곡은 카날라-브란트로 알려진 네 가지 매개변수 왜곡 모델을 사용하여 모델링된다.
OpenCV는 "fisheye" 모듈에서 이러한 왜곡 모델을 지원하며, 자세한 내용은 여기에서 확인할 수 있다.
https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html
"""

"""
Returns R, T transform from src to dst
"""
def get_extrinsics(src, dst):
    extrinsics = src.get_extrinsics_to(dst)
    R = np.reshape(extrinsics.rotation, [3,3]).T
    T = np.array(extrinsics.translation)
    return (R, T)

"""
Returns a camera matrix K from librealsense intrinsics
"""
def camera_matrix(intrinsics):
    return np.array([[intrinsics.fx, 0,                intrinsics.ppx],
                           [0,                intrinsics.fy, intrinsics.ppy],
                           [0,                0,                1]])

"""
Returns the fisheye distortion from librealsense intrinsics
"""
def fisheye_distortion(intrinsics):
    return np.array(intrinsics.coeffs[:4])

# Set up a mutex to share data between threads 
from threading import Lock
frame_mutex = Lock()
frame_data = {"left"  : None,
              "right" : None,
              "timestamp_ms" : None
              }

"""
이 콜백은 별도의 스레드에서 호출되므로, 데이터가 제대로 동기화되도록 뮤텍스를 사용해야 한다.
또한 콜백 대기열에서 데이터가 백업되지 않도록 이 스레드에서 많은 작업을 수행하지 않도록 주의해야 한다.
"""
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

#RealSense 파이프라인 선언, 실제 장치 및 센서 캡슐화
pipe = rs.pipeline()

# 구성 개체 구축 및 모든 스트림
cfg = rs.config()

# 콜백으로 스트리밍 시작
pipe.start(cfg, callback)

try:
    # 결과를 시각화하도록 OpenCV 창 설정
    WINDOW_TITLE = 'Realsense'
    cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)

    # OpenCV 스테레오 알고리즘을 구성하십시오.
    # 매개 변수에 대한 설명은 https://docs.opencv.org/3.4/d2/d85/classcv_1_1StereoSGBM.html을 참조하십시오.
    window_size = 5
    min_disp = 0
    # 16으로 나누어야 한다.
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

    # 두 카메라에 대한 스트림 및 고유 특성 검색
    profiles = pipe.get_active_profile()
    streams = {"left"  : profiles.get_stream(rs.stream.fisheye, 1).as_video_stream_profile(),
               "right" : profiles.get_stream(rs.stream.fisheye, 2).as_video_stream_profile()}
    intrinsics = {"left"  : streams["left"].get_intrinsics(),
                  "right" : streams["right"].get_intrinsics()}

    # 두 카메라에 대한 정보 인쇄
    print("Left camera:",  intrinsics["left"])
    print("Right camera:", intrinsics["right"])

    # "Librealsense"에서 "OpenCV"로 본질 변환
    K_left  = camera_matrix(intrinsics["left"])
    D_left  = fisheye_distortion(intrinsics["left"])
    K_right = camera_matrix(intrinsics["right"])
    D_right = fisheye_distortion(intrinsics["right"])
    (width, height) = (intrinsics["left"].width, intrinsics["left"].height)

    # 좌측 및 우측 카메라 사이의 상대적 외연성 가져오기
    (R, T) = get_extrinsics(streams["left"], streams["right"])

    # 우리는 카메라 매트릭스를 initUndistortRectifyMap에 설정하기 위해 왜곡되지 않은 우리의 이미지들이
    # 어느 정도의 초점 길이를 가져야 하는지 결정해야 한다.
    # 스테레오보정(steeroRecify)을 사용할 수 있지만,
    # 여기서는 보정 및 원하는 높이와 시야에서 이러한 투영 매트릭스를 도출하는 방법을 보여 준다.

    # 왜곡되지 않은 초점 길이를 계산한다.
    #
    #         h
    # -----------------
    #  \      |      /
    #    \    | f  /
    #     \   |   /
    #      \ fov /
    #        \|/
    stereo_fov_rad = 90 * (pi/180)  # 90 degree desired fov
    stereo_height_px = 300          # 300x300 pixel stereo output
    stereo_focal_px = stereo_height_px/2 / tan(stereo_fov_rad/2)

    # 좌측 회전은 아이덴티티로 설정하고 우측 회전은 카메라 사이의 회전으로 설정한다.
    R_left = np.eye(3)
    R_right = R

    # 스테레오 알고리즘은 원하는 출력 영역에서 유효한 차이를 만들기 위해 max_disp 여분의 픽셀을 필요로 한다.
    # 이렇게 하면 너비가 변경되지만 투영 중심은 잘라낸 이미지의 중심에 있어야 한다.
    stereo_width_px = stereo_height_px + max_disp
    stereo_size = (stereo_width_px, stereo_height_px)
    stereo_cx = (stereo_height_px - 1)/2 + max_disp
    stereo_cy = (stereo_height_px - 1)/2

    # 왼쪽 및 오른쪽 투영 행렬을 구성하며, 유일한 차이점은 오른쪽 투영 행렬이 기준선*focal_length의 x 축을 따라 이동해야 한다.
    P_left = np.array([[stereo_focal_px, 0, stereo_cx, 0],
                       [0, stereo_focal_px, stereo_cy, 0],
                       [0,               0,         1, 0]])
    P_right = P_left.copy()
    P_right[0][3] = T[0]*stereo_focal_px

    # cv2.reprojectImageTo3D와 함께 사용할 Q를 구성하십시오.
    # 나중에 차이를 줄일 것이므로 x에서 max_disp를 빼십시오.
    Q = np.array([[1, 0,       0, -(stereo_cx - max_disp)],
                  [0, 1,       0, -stereo_cy],
                  [0, 0,       0, stereo_focal_px],
                  [0, 0, -1/T[0], 0]])

    # 수리를 적용하고 카메라 왜곡을 해제하는 왼쪽 및 오른쪽 카메라에 대한 왜곡되지 않은 지도를 만드십시오.
    # 이 일은 한 번만 하면 된다.
    m1type = cv2.CV_32FC1
    (lm1, lm2) = cv2.fisheye.initUndistortRectifyMap(K_left, D_left, R_left, P_left, stereo_size, m1type)
    (rm1, rm2) = cv2.fisheye.initUndistortRectifyMap(K_right, D_right, R_right, P_right, stereo_size, m1type)
    undistort_rectify = {"left"  : (lm1, lm2), "right" : (rm1, rm2)}

    mode = "stack"
    while True:
        # 카메라에서 프레임을 획득했는지 확인하십시오.
        frame_mutex.acquire()
        valid = frame_data["timestamp_ms"] is not None
        frame_mutex.release()

        # 프레임을 처리할 준비가 된 경우
        if valid:
            # 스테레오 프레임을 복사할 수 있을 정도로만 뮤텍스를 길게 유지하십시오.
            frame_mutex.acquire()
            frame_copy = {"left"  : frame_data["left"].copy(),
                          "right" : frame_data["right"].copy()}
            frame_mutex.release()

            # 프레임의 중앙을 정렬 해제 및 자르기
            center_undistorted = {"left" : cv2.remap(src = frame_copy["left"],
                                          map1 = undistort_rectify["left"][0],
                                          map2 = undistort_rectify["left"][1],
                                          interpolation = cv2.INTER_LINEAR),
                                  "right" : cv2.remap(src = frame_copy["right"],
                                          map1 = undistort_rectify["right"][0],
                                          map2 = undistort_rectify["right"][1],
                                          interpolation = cv2.INTER_LINEAR)}

            # 프레임 중앙의 차이를 계산하여 픽셀 격차로 변환(DISP_SCLE=16으로 구분)
            disparity = stereo.compute(center_undistorted["left"], center_undistorted["right"]).astype(np.float32) / 16.0

            # 그 격차의 유효 부분만을 재평가
            disparity = disparity[:,max_disp:]

            # 차이를 0으로 환산하여 색칠
            disp_vis = 255*(disparity - min_disp)/ num_disp
            disp_color = cv2.applyColorMap(cv2.convertScaleAbs(disp_vis,1), cv2.COLORMAP_JET)
            color_image = cv2.cvtColor(center_undistorted["left"][:,max_disp:], cv2.COLOR_GRAY2RGB)
            

            if mode == "stack":
                cv2.imshow(WINDOW_TITLE, np.hstack((color_image, disp_color)))

            if mode == "overlay":
                ind = disparity >= min_disp
                color_image[ind, 0] = disp_color[ind, 0]
                color_image[ind, 1] = disp_color[ind, 1]
                color_image[ind, 2] = disp_color[ind, 2]
                cv2.imshow(WINDOW_TITLE, color_image)            
        
        key = cv2.waitKey(1)
        if key == ord('s'): mode = "stack"
        if key == ord('o'): mode = "overlay"
        if key == ord('q') or cv2.getWindowProperty(WINDOW_TITLE, cv2.WND_PROP_VISIBLE) < 1:
            break
        
finally:
    pipe.stop()
