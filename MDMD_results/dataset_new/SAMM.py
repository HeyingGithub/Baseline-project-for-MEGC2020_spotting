'''
Copyright (c) 2019.11 Ying He (heyingyouxiang@qq.com). All rights reserved.
'''

# handle the SAMM dataset
from use_mode import USE_MODE
if USE_MODE=='all' or USE_MODE=='generate':
    import xlrd
    from sklearn.model_selection import train_test_split
if USE_MODE=='all' or USE_MODE=='use':
    from glob import glob
if USE_MODE == 'evaluate':
    pass
import os
import random
import dataset_helper as dtset_hp


current_path = os.path.split(os.path.realpath(__file__))[0]
SOURCE_DATA = "{}/data/SAMM".format(current_path)
SAVE_SETS = "{}/data/SAMM_Sets".format(current_path)
DEFAULT_RATIO = 0.7
DEFAULT_FOLDER_K = 5


class SAMM(object):

    def __init__(self, mode="all", trainTestRatio = DEFAULT_RATIO, folder_k=DEFAULT_FOLDER_K, reSplit = False):

        if not os.path.exists(SAVE_SETS):
            os.makedirs(SAVE_SETS)
            self.generate_dataset()
            reSplit = True

        if reSplit == True:
            self.split_dataset(mode,trainTestRatio,folder_k)


    # read the excel file "SAMM_Micro_FACS_Codes.xlsx" and generate the four files: "allInfo.txt", "SAMM_all.txt", "micro_all.txt"
    def generate_dataset(self):

        wb = xlrd.open_workbook(SOURCE_DATA + "/SAMM_Micro_FACS_Codes.xlsx")
        sheet_micro = wb.sheet_by_name('MICRO_ONLY')
        nrows = sheet_micro.nrows

        allInfo = []
        micro_all = []
        SAMM_all = []

        for row_id in range(nrows):
            if row_id<=10:
                continue
            folder = sheet_micro.cell_value(row_id,0)
            video = str(sheet_micro.cell_value(row_id,1)).split('_')[1]
            cls = "micro-expression"
            onset_frame = sheet_micro.cell_value(row_id,3)
            apex_frame = sheet_micro.cell_value(row_id,4)
            offset_frame = sheet_micro.cell_value(row_id,5)

            info_line = "{} {} {} {} {} {}\n".format(folder, video, cls, 
                onset_frame, apex_frame, offset_frame)
            allInfo.append(info_line)

            video_line = "{} {}\n".format(folder, video)
            micro_all.append(video_line)

        root, folders, _ = dtset_hp.return_oswalk(SOURCE_DATA)
        for folder in folders:
            videos_path = os.path.join(root, folder)
            _, videos, _ = dtset_hp.return_oswalk(videos_path)
            for video in videos:
                video_line = "{} {}\n".format(folder, video)
                SAMM_all.append(video_line)


        micro_all = list(set(micro_all))

        dtset_hp.write_lines(SAVE_SETS+"/all_Info.txt", allInfo)
        dtset_hp.write_lines(SAVE_SETS+"/SAMM_all.txt", SAMM_all)
        dtset_hp.write_lines(SAVE_SETS+"/micro_all.txt", micro_all)


    # The parameter "mode" has five options: "all", "hold_out", "k_fold", "LOSO", "LOVO".
    # 
    # "all" means generate all the four kinds of validation sets as follows, and others mean which one to generate:
    # (1) Hold-Out Method, (2) K-fold Cross Validation, (3) leave-one-subject-out (LOSO), (4) leave-one-video-out (LOVO)
    # 
    # (1) "Hold-Out Method" mode generates three files: "SAMM_hold_out.txt", "micro_hold_out.txt" and "macro_hold_out.txt". The lines in each file are: 
    # trainval:
    # video1
    # video2 
    # ...
    # videok
    # test:
    # video1
    # video2
    # ...
    # videok
    # (2) "K-fold Cross Validation" mode generates three files: "SAMM_k_fold.txt", "micro_k_fold.txt" and "macro_k_fold.txt". The lines in each file are:
    # folder1:
    # video1
    # video2 
    # ...
    # videon
    # folder2:
    # video1
    # video2
    # ...
    # videon
    # .
    # .
    # folderk:
    # video1
    # video2
    # ...
    # videon
    # (3) "leave-one-subject-out" mode generates three files:  "SAMM_LOSO.txt", "micro_LOSO.txt" and "macro_LOSO.txt". The lines in each file are:
    # subject1:
    # video1
    # video2 
    # ...
    # videon
    # subject2:
    # video1
    # video2
    # ...
    # videon
    # .
    # .
    # subjectk:
    # video1
    # video2
    # ...
    # videon
    # (4) "leave-one-video-out" mode generates three files:  "SAMM_LOVO.txt", "micro_LOVO.txt" and "macro_LOVO.txt". The lines in each file are:
    # video1
    # video2 
    # ...
    # videon
    def split_dataset(self,mode,ratio,folder_k):

        micro = dtset_hp.read_lines(SAVE_SETS+"/micro_all.txt")
        SAMM_all = dtset_hp.read_lines(SAVE_SETS+"/SAMM_all.txt")

        # (1) Hold-Out Method
        def hold_out(ratio):
            folder_hold_out = SAVE_SETS+"/Hold-Out"
            if not os.path.exists(folder_hold_out): os.makedirs(folder_hold_out)

            micro_train, micro_test = train_test_split(micro,test_size=1-ratio,random_state=0)
            SAMM_train, SAMM_test = train_test_split(SAMM_all,test_size=1-ratio,random_state=0)

            micro_hold_out = ['trainval:\n'] + micro_train + ['test:\n'] + micro_test
            SAMM_hold_out = ['trainval:\n'] + SAMM_train + ['test:\n'] + SAMM_test

            dtset_hp.write_lines(folder_hold_out+"/SAMM_hold_out.txt", SAMM_hold_out)
            dtset_hp.write_lines(folder_hold_out+"/micro_hold_out.txt", micro_hold_out)

        # (2) K-fold Cross Validation
        def k_fold(folder_k):
            folder_k_fold = SAVE_SETS+"/K-fold"
            if not os.path.exists(folder_k_fold): os.makedirs(folder_k_fold)

            def folder_k_lines(dataset):
                random.shuffle(dataset)
                n = int(len(dataset)/folder_k)
                r = len(dataset)%folder_k
                lines = []
                a = 1
                start = 0
                for i in range(folder_k-1):
                    if r==0: a = 0
                    else: r = r-1
                    lines = lines + ['folder{}:\n'.format(i+1)] + dataset[start:start+n+a]
                    start = start+n+a
                lines = lines + ['folder{}:\n'.format(i+2)] + dataset[start:len(dataset)]
                return lines

            dtset_hp.write_lines(folder_k_fold+"/SAMM_k_fold.txt", folder_k_lines(SAMM_all))
            dtset_hp.write_lines(folder_k_fold+"/micro_k_fold.txt", folder_k_lines(micro))

        # (3) leave-one-subject-out (LOSO)
        def LOSO():
            folder_LOSO = SAVE_SETS+"/LOSO"
            if not os.path.exists(folder_LOSO): os.makedirs(folder_LOSO)

            def loso_lines(dataset):
                random.shuffle(dataset)
                map_subject = {}
                for line in dataset:
                    subject = line.split()[0]
                    if subject in map_subject: 
                        map_subject[subject].append(line)
                    else: 
                        map_subject[subject] = [line]
                lines = []
                for i, value in enumerate(map_subject.values()):
                    lines = lines + ['subject{}:\n'.format(i+1)] + value
                return lines

            dtset_hp.write_lines(folder_LOSO+"/SAMM_LOSO.txt", loso_lines(SAMM_all))
            dtset_hp.write_lines(folder_LOSO+"/micro_LOSO.txt", loso_lines(micro))

        # (4) leave-one-video-out (LOVO)
        def LOVO():
            folder_LOVO = SAVE_SETS+"/LOVO"
            if not os.path.exists(folder_LOVO): os.makedirs(folder_LOVO)

            random.shuffle(SAMM_all)
            random.shuffle(micro)

            dtset_hp.write_lines(folder_LOVO+"/SAMM_LOVO.txt", SAMM_all)
            dtset_hp.write_lines(folder_LOVO+"/micro_LOVO.txt", micro)

        if mode=="all":
            hold_out(ratio)
            k_fold(folder_k)
            LOSO()
            LOVO()
        elif mode=="hold_out":
            hold_out(ratio)
        elif mode=="k_fold":
            k_fold(folder_k)
        elif mode=="LOSO":
            LOSO()
        elif mode=="LOVO":
            LOVO()
        else:
            raise Exception('Eorror! "mode" only has five options: "all", "hold_out", "k_fold", "LOSO" and "LOVO".')


    # Function: produce a video list like [video1,video2,...], or produce some video sets each of which is a dictionary like 
    #           {"setname1":[video1,video2,...],"setname2":[video1,video2,...],...}. 
    #           
    #           A video is represented by ('folder', 'name_code'), like ['006', '1']). 
    #           So a video list [video1,video2,...] is like [['folder1', 'code1'],['folder2', 'code2'], ...].
    # Input:
    #        The parameter "videotype" has two options: "SAMM" and "micro".
    #        The parameter "whichSplit" has five options: "all", "hold_out", "k_fold", "LOSO" and "LOVO".
    # Output:
    #        (1) If the parameter "whichSplit" is set to "all": return a video list like [video1,video2,...];
    #        (2) If the parameter "whichSplit" is set to "hold_out": return two video sets like {"trainval:":videolist1,"test:":videolist2};
    #        (3) If the parameter "whichSplit" is set to "k_fold": return k video sets like {"folder1:":videolist1,"folder2:":videolist2, ..., "folderk:":videolistk};
    #        (4) If the parameter "whichSplit" is set to "LOSO": return several video sets like {"subject1:":videolist1,"subject2:":videolist2, ...};
    #        (5) If the parameter "whichSplit" is set to "LOVO": return a video list like [video1,video2, ...];
    def produce_videos(self,videotype,whichSplit): 

        whichSplit_folder_map = {"all":"", "hold_out":"Hold-Out/", "k_fold":"K-fold/", "LOSO":"LOSO/", "LOVO":"LOVO/"}
        filename = "{}/{}{}_{}.txt".format(SAVE_SETS, whichSplit_folder_map[whichSplit], videotype, whichSplit)

        def line_to_video(line):
            folder = line.split()[0]
            code = line.split()[1].strip('\n')
            return [folder, code]


        def toVideoList(filename):
            videolist = []
            for line in dtset_hp.read_lines(filename): videolist.append(line_to_video(line))
            return videolist


        def toSetsDict(filename):
            videodict = {}
            for line in dtset_hp.read_lines(filename):
                if line.find(":")!=-1:
                    current_key = line.strip('\n')
                    videodict[current_key] = []
                else:
                    videodict[current_key].append(line_to_video(line))
            return videodict

        if not os.path.exists(filename):
            raise Exception("There doesn't exist the file:" + filename + 
                '\nOptions for the parameter "videotype": "SAMM", "micro".' + 
                '\nOptions for the parameter "whichSplit": "all", "hold_out", "k_fold", "LOSO", "LOVO".')

        return toVideoList(filename) if whichSplit=="all" or whichSplit=="LOVO" else toSetsDict(filename)


    # ['folder1', 'code1'] ---> a list of image paths. Example: video_to_imagePaths(['s15', '0102'])
    # ['folder1', 'code1'] ---> a list of image paths or names. Example: video_to_imagePaths(['s15', '0102'])
    # The parameter "imgMode" has two options: "fullPaths" and "imgNames".
    def video_to_images(self,video,imgMode):

        def sort_img_rule(x):
            return int(x.split('_')[-1].split('.')[0])

        images_path = "{}/{}/{}/*.jpg".format(SOURCE_DATA,video[0],video[1])
        sorted_fullPaths = sorted(glob(images_path),key=sort_img_rule)

        if imgMode=="fullPaths": return sorted_fullPaths
        elif imgMode=="imgNames": return [path.split('/')[-1] for path in sorted_fullPaths]
        else: raise Exception('Eorror! "imgMode" only has two options: "fullPaths" and "imgNames".')


    # Return the number of the frames in the given video.
    def num_frames(self,video):
        return len(self.video_to_images(video,"fullPaths"))


    # ['folder1', 'code1'] ---> a list of labels: [[class1, onset1, apex1, offset1],[class2, onset2, apex2, offset2],...]
    def video_to_labels(self,video):
        labels = []
        for line in dtset_hp.read_lines(SAVE_SETS + "/all_Info.txt"):
            ls = line.strip('\n').split(' ')
            folder = ls[0]
            code = ls[1]
            if folder == video[0] and code == video[1]:
                cls = ls[2]
                onset = float(ls[3])
                apex = float(ls[4])
                offset = float(ls[5])
                labels.append([cls,onset,apex,offset])
        return labels


    # [video1, video2, ...] ---> a list of expressions: [[class1, video1, onset1, apex1, offset1],[class2, video2, onset2, apex2, offset2],...] (A video is represented by ['folder1', 'code1']).
    # The parameter "cls" has two options: "SAMM" and "micro".
    def videolist_to_expressions(self,videolist,cls):
        if cls not in ["SAMM", "micro"]: raise Exception('Eorror! "cls" only has two options: "SAMM" and "micro".')
        cls_map = {"micro":"micro-expression"}
        expression_list = []
        for video in videolist:
            labels = self.video_to_labels(video)
            for label in labels:
                c_truth = label[0]
                if cls!="SAMM" and cls_map[cls]!=c_truth: continue
                label.insert(1,video)
                expression_list.append(label)
        return expression_list


    # Returns a list of image paths or names from the onset to the offset in the video, like ['imageName1','imageName2',...].
    # The parameter "imgMode" has two options: "fullPaths" and "imgNames".
    # the minist onset is 0, according to image naming rules
    def interval_to_images(self,video,onset,offset,imgMode):

        def num_to_imgname(num, imgMode='imageName'):
            def sort_img_rule(x):
                return int(x.split('_')[-1].split('.')[0])

            img_num = '%04d' % num
            images_path = "{}/{}/{}/*{}.jpg".format(SOURCE_DATA,video[0],video[1],img_num)
            images_fullpath = sorted(glob(images_path),key=sort_img_rule)[0]

            if imgMode=="fullPaths": return images_fullpath
            elif imgMode=="imgNames": return images_fullpath.split('/')[-1]
            else: raise Exception('Eorror! "imgMode" only has two options: "fullPaths" and "imgNames".')

        onset = int(onset)
        offset = int(offset)
        if offset<onset or onset<0 or offset>self.num_frames(video)-1:
            raise Exception('Eorror! "onset" or "offset" is wrong.')

        img_list = []
        for i in range(onset,offset+1):
            img_name = num_to_imgname(i,imgMode)
            img_list.append(img_name)

        return img_list


    # input: (1) video, (2) the sequence number (start from 1) of the frame of the video to generate infomation
    # output: a infomation dictionary { 'isInTruth': True(False), 'isOnset': True(False), 'isApex': True(False), 'isOffset': True(False), 'class': 'micro-expression'('background'), 'interval': [onset, offset], 'interval_apex': apex }
    def frame_info(self,video,frame_iNo):
        labels = self.video_to_labels(video)
        info_dic = { 'isInTruth': False, 'isOnset': False, 'isApex': False, 'isOffset': False, 'class': 'background', 'interval': [-1, -1], 'interval_apex': -1 }
        for label in labels:
            onset = int(label[1])
            offset = int(label[3])
            if frame_iNo >= onset and frame_iNo <= offset:
                cls = label[0]
                apex = int(label[2])
                info_dic['isInTruth'] = True
                if frame_iNo == onset: info_dic['isOnset'] = True
                if frame_iNo == apex: info_dic['isApex'] = True
                if frame_iNo == offset: info_dic['isOffset'] = True
                info_dic['class'] = cls
                info_dic['interval'] = [onset, offset]
                info_dic['interval_apex'] = apex
                break
        return info_dic


'''#test
samm=SAMM()
#print(samm.produce_videos('SAMM','LOSO'))
#print(samm.video_to_images(['006', '1'],'imgNames')) # 'imgNames' or 'fullPaths'
#print(samm.num_frames(['006', '1']))
#print(samm.video_to_labels(['006', '1']),'\n',samm.video_to_labels(['006', '4']))
#print(samm.videolist_to_expressions(samm.produce_videos('SAMM','LOSO')['subject1:'],'SAMM'))
#print(samm.interval_to_images(['006', '1'],1,33,'imgNames'))
#print(samm.frame_info(['006', '1'],7260))
print(samm.num_frames(['006', '1']))
#'''