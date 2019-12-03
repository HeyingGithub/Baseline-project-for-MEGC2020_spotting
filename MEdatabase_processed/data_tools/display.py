'''
This script is to help people see the cropped faces or various kinds of flows visually. 
'''
import sys
sys.path.append("../dataset")
import cv2
import argparse
import data_provider as dt
import tool_helper as hp


parser = argparse.ArgumentParser(description='')
parser.add_argument('--what_display', dest='what_display', default='crop_face', 
                     help='choices: crop_face, flow (the default is "crop_face")')
parser.add_argument('--flow_from', dest='flow_from', default='none', 
                     help='choices: none, img (the default is "none")')
parser.add_argument('--win_size', dest='win_size', type=int, default=2, 
                     help='how many images for a flow (the default value is 2)')
parser.add_argument('--only_expressions', dest='only_expressions', type=bool, default=False, 
                     help='choose whether to only display facial expressions (the default is False)')

args = parser.parse_args()
what_display = args.what_display
flow_from = args.flow_from
win_size = args.win_size
only_expressions = args.only_expressions


me2 = dt.DataProvider('ME2')
videos = me2.produce_videos('ME2','all')

for video in videos:
    num_frames = me2.num_frames(video)
    if num_frames < win_size: continue

    if what_display == 'crop_face' or (what_display == 'flow' and flow_from == 'none'):
        read_folder = '../processed_data/crop_faces/{}/{}'.format(video[0],video[1])
    elif what_display == 'flow' and flow_from == 'img':
        read_folder = '../processed_data/for_people/flow_img/size{}/{}/{}'.format(win_size,video[0],
                                                                                   video[1])

    frames = me2.video_to_frames(video,"imgNames")
    isOnset = False # flag

    for i in range(num_frames):

        f_info = me2.frame_info(video,i+1)
        read_name = frames[i].split('.')[0]

        if only_expressions==True and f_info['isInTruth']== False: continue

        if (what_display == 'crop_face') or (what_display == 'flow' and flow_from == 'img'):
            read_path = '{}/{}.jpg'.format(read_folder,read_name)
            img = cv2.imread(read_path)
         
        elif what_display == 'flow' and flow_from == 'none':
            win_flow = hp.win_flow(read_folder,frames,num_frames,win_size,i)
            img = hp.flow_to_img(win_flow)

        cv2.imshow('Image:',img)
        cv2.waitKey(20)

        cls = f_info['class']
        if f_info['isOnset']==True:
            isOnset = True
            print('{} {}_{}_{} {} onset!'.format(hp.now_time(),video[0],video[1],read_name,cls))
        if f_info['isOffset']==True:
            isOnset = False
            print('{} {}_{}_{} {} offset!'.format(hp.now_time(),video[0],video[1],read_name,cls))
        if ((not (only_expressions or isOnset)) and ((i+1)%100==0 or i+1==num_frames)):
            print("{} video: {}, frame: {}".format(hp.now_time(), video, i+1))
print('Finish all.')
