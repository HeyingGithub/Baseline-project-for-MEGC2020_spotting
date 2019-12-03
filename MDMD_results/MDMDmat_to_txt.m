clear
clc

%dataset = 'ME2';
dataset = 'SAMM_MEGC';
%dataset = 'SAMM';

%cl = 'micro';
cl = 'macro';

[video_names, nums_frames] = textread(['../../MEdatabase_processed/', dataset, '.txt'], '%s%d');
mat_folder = ['results_mat/', dataset, '_', cl, '_results'];
txt_folder = ['results_API/', dataset, '_', cl, '_txtClips'];
if ~exist(txt_folder, 'dir')
    mkdir(txt_folder);
end

num_videos = length(video_names);
for i=1:num_videos
    
    video_name = char(video_names(i));
    mat_file = [mat_folder, '/', video_name, '_prd.mat'];
    if ~exist(mat_file, 'file')
        continue;
    end
    
    load(mat_file);
    n_thresh = size(predicts,1);
    
    for j=1:n_thresh
%         thresh = predicts{j,2};
        predict = predicts{j,3};
        
        save_folder = [txt_folder, '/p', num2str(j)];       
        if i==1 && ~exist(save_folder, 'dir')
            mkdir(save_folder);
        end
        
        f_txt = fopen([save_folder, '/', video_name, '.txt'], 'w');
        has_onset = false;
        for k=1:length(predict)
            if predict(k) == 1 && has_onset == false
                has_onset = true;
                onset = k;
            end
            if  predict(k) == 0 && has_onset == true
                has_onset = false;
                offset = k-1;
                fprintf(f_txt, sprintf('%d %d 1.0\n', onset, offset));
            end
        end
        fclose(f_txt);
    end
end