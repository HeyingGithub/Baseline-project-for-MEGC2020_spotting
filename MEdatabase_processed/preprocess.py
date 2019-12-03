import sys
sys.path.append("./data_tools")
sys.path.append("./dataset_new")
import cv2
import os
import Module_crop_times as mycrop
import data_provider as dt
import tool_helper as hp


#dataset = 'ME2'
#dataset = 'SAMM'
dataset = 'SAMM_MEGC'


crop_times = 2
resize = 227


data_handler = dt.DataProvider(dataset)
videos = data_handler.produce_videos(dataset,'all')


for video in videos:
    num_frames = data_handler.num_frames(video)
    if num_frames == 0: continue

    frames = data_handler.video_to_frames(video)
    frame_0 = cv2.imread(frames[0])
    ymin, ymax, xmin, xmax = mycrop.crop_times(frame_0, crop_times)

    save_folder = './processed_data/{}_crop_faces/{}/{}'.format(dataset,video[0],video[1])
    if not os.path.exists(save_folder): os.makedirs(save_folder)
    save_folder_examples = './processed_data/for_people/{}_crop_examples'.format(dataset)
    if not os.path.exists(save_folder_examples): os.makedirs(save_folder_examples)

    for i in range(num_frames):
        frame = cv2.imread(frames[i])
        crop_frame = frame[ymin:ymax, xmin:xmax]
        save_frame = cv2.resize(crop_frame,(resize,resize))
        
        if i==0: cv2.imwrite('{}/{}_{}.jpg'.format(save_folder_examples,video[0],video[1]), save_frame)
        img_name = frames[i].split('/')[-1]
        save_path = '{}/{}'.format(save_folder,img_name)
        cv2.imwrite(save_path, save_frame)

        if (i+1)%1000==0 or i+1==num_frames:
             print("{} video: {}, frame: {}".format(hp.now_time(), video, i+1))
    print('Finish video: {}.'.format(video))
print('Finish all.')
