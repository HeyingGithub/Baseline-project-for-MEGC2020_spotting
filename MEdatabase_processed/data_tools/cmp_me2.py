'''
The function of this script is: save facial expressions (cropped faces and vrious kinds of flows) to the folder "../processed_data/for_people/cmp_me2" for comparison. 

There is a "extend_num" to extend the onset and the offset.
'''
import sys
sys.path.append("..")
import cv2
import os
import shutil
import dataset.data_provider as dt
import tool_helper as hp

#use_dataset = 

# "dataset" options: "ME2", "SAMM"
def num_to_imgname(num, dataset):
    img_num = '%03d' %num if num < 100 else str(num)
    return 'img'+img_num+'.jpg'

me2 = dt.DataProvider('ME2')
videos = me2.produce_videos('ME2','all')

extend_num = 0 #10
map_paths = {'../processed_data/crop_faces':                   'crop_faces',
             #'../processed_data/for_people/flow_img/size2':    'flow_win2',
             #'../processed_data/for_people/flow_img/size5':    'flow_win5',
             #'../processed_data/for_people/flow_img/size7':    'flow_win7',
             #'../processed_data/for_people/flow_img/size10':   'flow_win10',
             #'../processed_data/for_people/flow_img/size15':   'flow_win15',
            }
save_path = '../processed_data/for_people/cmp_me2'

for video in videos:
    num_frames = me2.num_frames(video)
    if num_frames < 2: continue

    labels = me2.video_to_labels(video)

    for i,label in enumerate(labels):
        cls = label[0]
        onset = int(label[1])
        offset = int(label[3])

        onset_extend = onset - extend_num if (onset - extend_num) >= 0 else 0
        offset_extend = offset + extend_num if (offset + extend_num) <= num_frames else num_frames

        for img_num in range(onset_extend, offset_extend+1):
            img_name = num_to_imgname(img_num)
            img_path_name0 = '{}/{}/{}'.format(video[0],video[1],img_name)
            save_img_path0 = '{}_{}_{}'.format(video[0],video[1],i)
            for key in map_paths:
                img_path_name = '{}/{}'.format(key,img_path_name0)
                save_img_path = '{}/{}/{}/{}'.format(save_path,cls,map_paths[key],save_img_path0)
                if not os.path.exists(save_img_path): os.makedirs(save_img_path)
                if os.path.exists(img_path_name): 
                    shutil.copy(img_path_name,save_img_path)
                else:
                    print('No such file: {}'.format(img_path_name))
    print('{} Finish video:{}'.format(hp.now_time(), video))
print('Finish all!')
