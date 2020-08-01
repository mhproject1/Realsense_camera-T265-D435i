import matplotlib.pyplot as plt
import pyrealsense2 as rs
import time

cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

pipe = rs.pipeline()
pipe.start(cfg)

try:
    while(1):
        frames = pipe.wait_for_frames()
        pose = frames.get_pose_frame()

        if pose:
            data = pose.get_pose_data()
            print("x : ", data.translation.x, " y : ", data.translation.y)

finally:
    pipe.stop()
