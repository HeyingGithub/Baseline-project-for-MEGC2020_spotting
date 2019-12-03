import sys
sys.path.append("./dataset_new")
import os
import result_helper as hp
import data_provider as dt

#dataset = 'ME2'
dataset = 'SAMM_MEGC'
#dataset = 'SAMM'

#cls = 'micro'
cls = 'macro'
thresh = 0.5
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


folder = './eval_res_txt'
if not os.path.exists(folder): os.makedirs(folder)
res_file = '{}/{}_{}_all_p.txt'.format(folder, dataset, cls)
data_handler = dt.DataProvider(dataset)
videos = data_handler.produce_videos(dataset,'all')


f = open(res_file, 'w')
for p in range(1,100):
    txt_folder = './results_API/{}_{}_txtClips/p{}'.format(dataset, cls, p)

    pred_clips, true_labels, _ = hp.return_preds_labels(txt_folder, videos, cls, data_handler, False, shortest_len, longest_len)
    N_clips, N_correct_clips, N_labels, N_find_labels, _, _, recall, precision_large, precision_small, F1_large, F1_small = hp.pred_clips_analysis(pred_clips, true_labels, thresh)

    f.write('shortest {}, p={}:\n'.format(shortest_len, p))
    f.write('number of videos: {}\n'.format(len(true_labels)))
    f.write('{} {} {} {} {} {}\n\n'.format(N_clips, N_correct_clips, N_labels, recall, precision_small, F1_small))
f.close()
print('Finish.')