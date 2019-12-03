import cv2
import numpy as np
import time


def now_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


def flow(RGBimg_prvs, RGBimg_next):
    gray_prvs = cv2.cvtColor(RGBimg_prvs, cv2.COLOR_BGR2GRAY)
    gray_next = cv2.cvtColor(RGBimg_next, cv2.COLOR_BGR2GRAY)
    flw = cv2.calcOpticalFlowFarneback(gray_prvs, gray_next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    return flw


# frame_i starts from 0, and 0 means the number representing 'img001.jpg'.
# When 'win_size=2', this function returns an ordinary flow without adding together.
def win_flow(read_folder, frames, num_frames, win_size, frame_i):
    epoch = min(win_size-1, num_frames-frame_i-1)
    if epoch==0:
        epoch = 1
        frame_i = frame_i-1
    for j in range(epoch):
        name_prvs = frames[frame_i+j].split('/')[-1]
        name_next = frames[frame_i+j+1].split('/')[-1]
        frame_prvs = cv2.imread(read_folder + '/' + name_prvs)
        frame_next = cv2.imread(read_folder + '/' + name_next)
        if j==0:
            w_flow = flow(frame_prvs, frame_next)
        else:
            w_flow = w_flow + flow(frame_prvs, frame_next)        
    return w_flow


def flow_to_img(flow):
    shapeF = flow.shape
    hsv = np.full((shapeF[0], shapeF[1], 3),255, dtype='uint8')
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    return rgb

