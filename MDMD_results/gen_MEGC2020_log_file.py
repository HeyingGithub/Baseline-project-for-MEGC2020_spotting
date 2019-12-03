import sys
sys.path.append("./dataset_new")
import os
import result_helper as hp
import data_provider as dt

datasets = ['SAMM_MEGC', 'ME2']
clss = ['micro', 'macro']
thresh = 0.5
p = 1


folder = './eval_res_txt'
if not os.path.exists(folder): os.makedirs(folder)
res_file = '{}/MEGC2020_MDMD_log_file.txt'.format(folder)
f = open(res_file, 'w')


for dataset in datasets:

    data_handler = dt.DataProvider(dataset)
    videos = data_handler.produce_videos(dataset,'all')
    No_dt = 1 if dataset == 'SAMM_MEGC' else 2
    f.write('{}\n'.format(No_dt))


    prd_info = {}
    for cls in clss:

        if dataset == 'ME2' and cls == 'micro':
            shortest_len = 7
            longest_len = 16
        elif dataset == 'ME2' and cls == 'macro':
            shortest_len = 17
            longest_len = -1
        elif (dataset == 'SAMM_MEGC' or dataset == 'SAMM') and cls == 'micro':
            shortest_len = 47
            longest_len = 105
        elif (dataset == 'SAMM_MEGC' or dataset == 'SAMM') and cls == 'macro':
            shortest_len = 106
            longest_len = -1

        txt_folder = 'results_API/{}_{}_txtClips/p{}'.format(dataset, cls, p)
        pred_clips, true_labels, videos = hp.return_preds_labels(txt_folder, videos, cls, data_handler, False, shortest_len, longest_len)
        prd_info[cls] = { "pred_clips": pred_clips, "true_labels": true_labels, "videos": videos }
        


    # prd_info -------> info_res
    info_res = { "label_pred_res": [], "videos": []} # "label_pred_res": [ [lb, prd, res], [lb, prd, res], ... ]

    for cls in clss:
        info = prd_info[cls]
        pred_clips = info["pred_clips"]
        true_labels = info["true_labels"]
        videos = info["videos"]

        def label_pair(label, preds):
            for prd in preds: 
                if hp.calc_iou(label, prd) >= thresh: return [label, prd, 'TP']
            return [label, [], 'FN']

        def prd_pair(pred, labels):
            for lb in labels: 
                if hp.calc_iou(pred, lb) >= thresh: return [lb, pred, 'TP']
            return [[], pred, 'FP']

        def sort_rule(pair):
            return pair[1][0] if pair[2] == 'TP' or pair[2] == 'FP' else pair[0][0]

        for video in videos:
            index = videos.index(video)
            preds = pred_clips[index]
            labels = true_labels[index]

            pairs = []
            for pred in preds: pairs.append(prd_pair(pred,labels))
            for label in labels:
                pair = label_pair(label, preds)
                if pair[2] == 'FN' or (pair not in pairs): pairs.append(pair)

            if video in info_res['videos']:
                index2 = info_res['videos'].index(video)
                info_res['label_pred_res'][index2] += pairs
            else:
                info_res['label_pred_res'].append(pairs)
                info_res['videos'].append(video)

    label_pred_res = info_res["label_pred_res"]
    for i in range(len(label_pred_res)):
        info_res["label_pred_res"][i] = sorted_pairs = sorted(label_pred_res[i],key=sort_rule)



    # write the log file
    videos = info_res['videos']
    label_pred_res = info_res['label_pred_res']
    for video in videos:
        index = videos.index(video)
        pairs = label_pred_res[index]

        for pair in pairs:
            lb = [ int(pair[0][0]), int(pair[0][1]) ] if pair[0] else ['-', '-']
            prd = pair[1] if pair[1] else ['-', '-']
            res = pair[2]

            line = '{}_{}   {}'.format(video[0].replace('s',''),video[1],lb[0])

            n = 18
            line += ' ' * (n-len(line))
            line += str(lb[1])

            n += 8
            line += ' ' * (n-len(line))
            line += str(prd[0])

            n += 8
            line += ' ' * (n-len(line))
            line += str(prd[1])

            n += 8
            line += ' ' * (n-len(line))
            line += res
            f.write(line+'\n')


f.close()
print('Finish.')