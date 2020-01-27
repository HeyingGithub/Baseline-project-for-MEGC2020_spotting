'''
Copyright (c) 2019.11 Ying He (heyingyouxiang@qq.com). All rights reserved.
'''

import numpy as np
import CASME_2
import SAMM
import SAMM_MEGC

dataset_names = ['ME2','SAMM','SAMM_MEGC']
DEFAULT_RATIO = 0.7
DEFAULT_FOLDER_K = 5

class DataProvider(object):

    # The "trainTestRatio" is useful only when we set "reSplit = True"
    def __init__(self, dataset_name, mode="all", trainTestRatio = DEFAULT_RATIO, folder_k=DEFAULT_FOLDER_K, reSplit = False):

        if dataset_name == dataset_names[0]:
            self.dataset = CASME_2.ME2(mode=mode, trainTestRatio = trainTestRatio, folder_k=folder_k, reSplit=reSplit)
        elif dataset_name == dataset_names[1]:
            self.dataset = SAMM.SAMM(mode=mode, trainTestRatio = trainTestRatio, folder_k=folder_k, reSplit=reSplit)
        elif dataset_name == dataset_names[2]:
            self.dataset = SAMM_MEGC.SAMM_MEGC(mode=mode, trainTestRatio = trainTestRatio, folder_k=folder_k, reSplit=reSplit)
        else:
            raise Exception("Error! The parameter 'dataset_name' isn't in: {}.".format(dataset_names))


    # For the CAS(ME)^2 and SAMM:
    # The parameter "mode" has five options: "all", "hold_out", "k_fold", "LOSO", "LOVO".
    def re_split_dataset(self,mode,ratio=DEFAULT_RATIO,folder_k=5):
        self.dataset.split_dataset(mode,ratio,folder_k)
        print('"ReSplit dataset" done!')


    # For the CAS(ME)^2: 
    # The parameter "cls" has three options: "ME2", "micro" and "macro".
    # The parameter "whichSplit" has five options: "all", "hold_out", "k_fold", "LOSO" and "LOVO".
    # For the SAMM: 
    # The parameter "cls" has two options: "SAMM" and "micro".
    # The parameter "whichSplit" has five options: "all", "hold_out", "k_fold", "LOSO" and "LOVO".
    def produce_videos(self, cls, whichSplit):
        return self.dataset.produce_videos(cls, whichSplit)


    # For the CAS(ME)^2 and SAMM:
    # ['folder1', 'code1'] ---> a list of labels: [[class1, onset1, apex1, offset1],[class2, onset2, apex2, offset2],...]
    def video_to_labels(self,video):
        return self.dataset.video_to_labels(video)


    def num_frames(self,video):
        return self.dataset.num_frames(video)


    # The parameter "imgMode" has two options: "fullPaths" and "imgNames".
    def video_to_frames(self, video, imgMode="fullPaths"):
        return self.dataset.video_to_images(video, imgMode)


    def frame_info(self,video,frame_iNo):
        return self.dataset.frame_info(video, frame_iNo)


    # For the CAS(ME)^2:
    # The parameter "cls" has three options: "ME2", "micro" and "macro".
    # [video1, video2, ...] ---> a list of expressions: [[class1, video1, onset1, apex1, offset1],[class2, video2, onset2, apex2, offset2],...] (A video is represented by ['folder1', 'code1']).
    # For the SAMM:
    # The parameter "cls" has two options: "SAMM" and "micro".
    # [video1, video2, ...] ---> a list of expressions: [[class1, video1, onset1, apex1, offset1],[class2, video2, onset2, apex2, offset2],...] (A video is represented by ['folder1', 'code1']).
    def videolist_to_actions(self,videolist,cls):
        return self.dataset.videolist_to_expressions(videolist, cls)


    # The parameter "imgMode" has two options: "fullPaths" and "imgNames".
    def interval_to_frames(self,video,onset,offset,imgMode="fullPaths"):
        return self.dataset.interval_to_images(video,onset,offset,imgMode)


'''#test ME2
me2 = DataProvider('ME2')
print(me2.frame_info(['s15', '0102'],699))
#'''

'''#test SAMM
samm = DataProvider('SAMM')
print(samm.frame_info(['006', '1'],699))
#'''

'''#test ME2
me2 = DataProvider('ME2')
videos = me2.produce_videos("ME2","all")
#print(me2.videolist_to_actions(videos,"micro"))
print(me2.interval_to_frames(['s15', '0102'],699,702,"fullPaths"))
'''

'''#test ME2
me2 = DataProvider('ME2')
video_dic = me2.produce_videos("micro","LOSO")
print(video_dic)
'''