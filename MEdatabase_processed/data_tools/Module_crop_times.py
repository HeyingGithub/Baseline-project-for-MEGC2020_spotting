import numpy as np
import cv2
import dlib
import os


current_path = os.path.split(os.path.realpath(__file__))[0]
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(current_path + '/shape_predictor_68_face_landmarks.dat')


def xs_ys(img_RGB):
    img_gray = cv2.cvtColor(img_RGB, cv2.COLOR_RGB2GRAY)
    xs = []
    ys = []
    rects = detector(img_gray, 0)
    for i in range(len(rects)):
        landmarks = np.matrix([[p.x, p.y] for p in predictor(img_RGB,rects[i]).parts()])

        for idx, point in enumerate(landmarks):
            xs.append(point[0, 0])
            ys.append(point[0, 1])
    return xs, ys


def crop_once(img_RGB):
    xs, ys = xs_ys(img_RGB)
    if len (xs)!= 0:
        ymin = min(ys)-(ys[36]-ys[18])
        ymax = max(ys)
        xmin = min(xs)
        xmax = max(xs)
        img_crop_RGB = img_RGB[max(ymin,0):min(ymax,img_RGB.shape[0]-1), 
                               max(xmin,0):min(xmax,img_RGB.shape[1]-1)]
    else:
        ymin = ymax = xmin = xmax = 0
        img_crop_RGB = img_RGB
    return img_crop_RGB, ymin, ymax, xmin, xmax


def max_more(img_crop_RGB, ymin_temp, ymax):
    img_crop2, ymin2, ymax2, xmin2, xmax2 = crop_once(img_crop_RGB)
    if ymax2 != 0:
        ymax = min(ymax, ymax2 + ymin_temp)
    return img_crop2, ymax, ymin2


def crop_times(img_RGB, times):
    img_crop_RGB, ymin, ymax, xmin, xmax = crop_once(img_RGB)

    ymin_temp = ymin
    for i in range(times-1):
        img_crop_RGB, ymax, ymin_new = max_more(img_crop_RGB, ymin_temp, ymax)
        ymin_temp = ymin_temp + max(ymin_new,0)

    return ymin, ymax, xmin, xmax
