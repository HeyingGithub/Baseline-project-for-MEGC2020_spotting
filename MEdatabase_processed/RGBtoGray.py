import sys
sys.path.append("./dataset_new")
import cv2
import os
import time
import data_provider as dt


#dataset = 'ME2'
#dataset = 'SAMM'
dataset = 'SAMM_MEGC'

data_handler = dt.DataProvider(dataset)
videos = data_handler.produce_videos(dataset,'all')

RGB_path = './processed_data/{}_crop_faces'.format(dataset)
gray_path = './processed_data/{}_crop_gray'.format(dataset)
if not os.path.exists(gray_path): os.makedirs(gray_path)


def now_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


for video in videos:

    img_names = data_handler.video_to_frames(video, 'imgNames')
    num_imgs = len(img_names)

    for i,img_name in enumerate(img_names):

        RGB_img_name = '{}/{}/{}/{}'.format(RGB_path, video[0], video[1], img_name)
        RGB_img = cv2.imread(RGB_img_name)

        gray_img = cv2.cvtColor(RGB_img, cv2.COLOR_BGR2GRAY)
        save_path = '{}/{}/{}'.format(gray_path, video[0], video[1])
        if not os.path.exists(save_path): os.makedirs(save_path)
        gray_img_name= '{}/{}'.format(save_path, img_name)
        cv2.imwrite(gray_img_name, gray_img)

        if (i+1)%1000==0 or i+1==num_imgs:
             print("{} video: {}, frame: {}".format(now_time(), video, i+1))
    print('Finish video: {}.'.format(video))
print('Finish all.')
