'''
The function of this script is: generate the images of the additive flows according to the cropped faces and the 'win_size', and save the images to the folder '../processed_data/for_people/flow_img'.
'''
import sys
sys.path.append("..")
import cv2
import os
import argparse
import dataset.data_provider as dt
import tool_helper as hp


parser = argparse.ArgumentParser(description='')
parser.add_argument('--win_size', dest='win_size', type=int, default=2, help='image numbers for a flow')
args = parser.parse_args()
win_size = args.win_size

me2 = dt.DataProvider('ME2')
videos = me2.produce_videos('ME2','all')

for video in videos:

    num_frames = me2.num_frames(video)
    if num_frames < win_size: continue
    frames = me2.video_to_frames(video)

    save_folder = '../processed_data/for_people/flow_img/size{}/{}/{}'.format(win_size,video[0],video[1])
    read_folder = '../processed_data/crop_faces/{}/{}'.format(video[0],video[1])
    if not os.path.exists(save_folder): os.makedirs(save_folder)

    for i in range(num_frames):
        win_flow = hp.win_flow(read_folder,frames,num_frames,win_size,i)
        img = hp.flow_to_img(win_flow)

        img_name = frames[i].split('/')[-1]
        save_path = '{}/{}'.format(save_folder,img_name)
        cv2.imwrite(save_path, img)

        if (i+1)%100==0 or i+1==num_frames:
             print("{} video: {}, frame: {}".format(hp.now_time(), video, i+1))

    print('Finish video: {}.'.format(video))
print('Finish all. (win_size = {})'.format(win_size))
