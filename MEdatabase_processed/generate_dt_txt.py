import sys
sys.path.append("./dataset_new")
import data_provider as dt


#dataset = 'ME2'
#dataset = 'SAMM'
dataset = 'SAMM_MEGC'

data_handler = dt.DataProvider(dataset)
videos = data_handler.produce_videos(dataset,'all')
videos_file = dataset + '.txt'

lines = []
for video in videos:
    num_frames = data_handler.num_frames(video)
    line = '{}_{} {}\n'.format(video[0], video[1], num_frames)
    lines.append(line)

with open(videos_file,'w') as fw: fw.writelines(lines)