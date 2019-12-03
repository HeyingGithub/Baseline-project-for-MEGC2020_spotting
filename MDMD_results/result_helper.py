import numpy as np
import os


def calc_iou(clip1, clip2):
    intersection = max(0, min(clip1[1], clip2[1]) - max(clip1[0], clip2[0])) + 1
    union = (clip1[1] - clip1[0] + 1) + (clip2[1] - clip2[0] + 1) - intersection 
    if clip1[1] <= clip1[0] or clip2[1] <= clip2[0] or union <= 0: return 0.0
    else: return float(intersection) / float(union)


def txt_to_clips(txt_file):
    lines = open(txt_file, 'r').readlines()
    clips = []
    scores = []
    for line in lines:
        ls = line.strip().split()
        clips.append([ int(ls[0]), int(ls[1]) ])
        scores.append(float(ls[2]))
    return clips, scores


# if length<shortest_len, delete it
def delete_short(clips, scores, shortest_len):
    clps = []
    scrs = []
    for i, clip in enumerate(clips):
        n = clip[1]-clip[0]+1
        if n>=shortest_len:
            clps.append(clip)
            scrs.append(scores[i])
    return clps, scrs


# if length<longest_len, delete it
def delete_long(clips, scores, longest_len):
    clps = []
    scrs = []
    for i, clip in enumerate(clips):
        n = clip[1]-clip[0]+1
        if n<=longest_len:
            clps.append(clip)
            scrs.append(scores[i])
    return clps, scrs



# Input1: pred_clips
#         A list: [ [clip1, clip2, ...], [clip1, clip2, ...], ... ]
# Input2: scores
#         a list: [ [score1, score2, ...], [score1, score2, ...], ... ]
#         'score' is the confidence score
# Output: nms_clips
#         A list: [ [clip1, clip2, ...], [clip1, clip2, ...], ... ]
def nms(clips, scores):

    output_clips = []

    for i in range(len(clips)):

        out_clips = []
        num_clips_batch = len(clips[i])

        for j in range(num_clips_batch):

            clip1 = clips[i][j]
            clip1_append = True

            for k in range(num_clips_batch):
                clip2 = clips[i][k]
                if k != j and calc_iou(clip1, clip2) >= st.nms_thresh and scores[i][j] < scores[i][k]:
                    clip1_append = False

            if clip1_append:
                out_clips.append(clip1)

        output_clips.append(out_clips)

    return output_clips




# Output1: pred_clips
#         A list: [ [clip1, clip2, ...], [clip1, clip2, ...], ... ]
#         A 'clip' is represented by [index0, index1], in which the index starts from 1 in the corresponding video clips.
# Output2: true_labels
#         A list: [ [ label1, label2 ], [ label1, label2 ], ... ]
#         The 'label' is represented by [index0,index1], in which the index starts from 1 in the corresponding video clips.
# Output3: videos
#         A list: [ video1, video2, ... ]
#         The 'label' is represented by [index0,index1], in which the index starts from 1 in the corresponding video clips.
def return_preds_labels(txt_folder, videos, cls, data_handler, if_nms = False, shortest_len=-1, longest_len=-1):
    pred_clips = []
    true_labels = []
    re_videos = []

    for video in videos:
        txt = '{}/{}_{}.txt'.format(txt_folder, video[0],video[1])
        if not os.path.exists(txt):
            print('Warnings: there is no file "{}", and it is skipped.'.format(txt))
            continue

        clips, scores = txt_to_clips(txt)
        if shortest_len !=-1: clips, scores = delete_short(clips, scores, shortest_len)
        if longest_len !=-1: clips, scores = delete_long(clips, scores, longest_len)
        if if_nms: clips = nms(clips, scores)

        lables = data_handler.video_to_labels(video)
        lbs = []
        for lb in lables:
            if lb[0] == cls+'-expression':
                lbs.append([ lb[1], lb[3]])

        pred_clips.append(clips)
        true_labels.append(lbs)
        re_videos.append(video)

    return pred_clips, true_labels, re_videos


# Input1: pred_clips
#         A list: [ [clip1, clip2, ...], [clip1, clip2, ...], ... ]
#         A 'clip' is represented by [index0, index1], in which the index starts from 1 in the corresponding video clips.
# Input2: true_labels
#         A list: [ [ label1, label2 ], [ label1, label2 ], ... ]
#         The 'label' is represented by [index0,index1], in which the index starts from 1 in the corresponding video clips.
# Input3: thresh
#         If calc_iou(clip, label) >= thresh, we think it predicts correctly.
# Output: (result infomation, 1 outputs:)
#         N_clips, N_correct_clips, N_labels, N_find_labels, pred_res, labels_res, recall, precision_large, precision_small, F1_large, F1_small
def pred_clips_analysis(pred_clips, true_labels, thresh):

    N_clips = 0
    N_correct_clips = 0
    N_labels = 0
    N_find_labels = 0
    pred_res = []
    labels_res = []


    for i in range(len(pred_clips)):

        labels = true_labels[i]

        # analyze
        num_clips_batch = len(pred_clips[i])
        num_labels_batch = len(labels)
        p_res = []
        l_res = []
        
        for label in labels:  
            N_labels = N_labels + 1
            l_res.append(0)

        true_lbs = np.zeros(num_labels_batch) # for record

        for j in range(num_clips_batch): # clip
            N_clips = N_clips + 1
            clip = pred_clips[i][j]
            p_res.append(0)

            for lb_index in range(num_labels_batch): # label
                label = labels[lb_index]
                if calc_iou(clip, label) >= thresh:
                    p_res[j] = p_res[j] + 1
                    l_res[lb_index] = l_res[lb_index] + 1

                    N_correct_clips = N_correct_clips + 1
                    true_lbs[lb_index] = 1

        N_find_labels = N_find_labels + int(sum(true_lbs))
        pred_res.append(p_res)
        labels_res.append(l_res)

    # evaluation
    recall = float(N_find_labels) / float(N_labels) if N_labels != 0 else 0
    precision_large = float(N_correct_clips) / float(N_clips) if N_clips != 0 else 0
    F1_large = 2 * recall * precision_large / (recall + precision_large) if (recall + precision_large) != 0 else 0
    precision_small = float(N_find_labels) / float(N_clips) if N_clips != 0 else 0
    F1_small = 2 * recall * precision_small / (recall + precision_small) if (recall + precision_small) != 0 else 0

    return N_clips, N_correct_clips, N_labels, N_find_labels, pred_res, labels_res, recall, precision_large, precision_small, F1_large, F1_small