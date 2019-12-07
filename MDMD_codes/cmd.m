clear
clc

%dataset = 'ME2';
dataset = 'SAMM_MEGC';
%dataset = 'SAMM';

cls = 'micro';
%cls = 'macro';

data_path = '../MEdatabase_processed';
result_path = '../MDMD_results/results_mat';

[video_names, nums_frames] = textread([data_path, '/', dataset, '.txt'], '%s%d');
videos_path = [data_path, '/processed_data/', dataset, '_crop_gray'];
save_path = [result_path, '/', dataset, '_', cls, '_results'];
if ~exist(save_path, 'dir')
    mkdir(save_path);
end

blocks=[6];
auto_k = true; % When the video is too short, halve the k until it is valid.
if strcmp(dataset, 'ME2') && strcmp(cls, 'micro')
    k=12;
elseif strcmp(dataset, 'ME2') && strcmp(cls, 'macro')
    k=39;
elseif (strcmp(dataset, 'SAMM') || strcmp(dataset, 'SAMM_MEGC')) && strcmp(cls, 'micro')
    k=80;
elseif (strcmp(dataset, 'SAMM') || strcmp(dataset, 'SAMM_MEGC')) && strcmp(cls, 'macro')
    k=260;
end
num_videos = length(video_names);

tic
for i=1:num_videos
    
    video_name = char(video_names(i));
    num_frames = nums_frames(i);
    video_spilt = strsplit(video_name,'_');
    images_path = [videos_path, '/', video_spilt(1), '/', video_spilt(2)];
    
    save_mat_name = [save_path, '/', video_name, '_prd.mat'];
    if exist(save_mat_name, 'file')
        continue;
    end

    l= num_frames-2*k;
    while auto_k && l-4*k<0
        k = round(k/2);
        l= num_frames-2*k;
    end
    
    RRR=MDMD(dataset, images_path, num_frames, k, blocks);
    MDMD_feature = zeros(l);
    
    for n1=1:l
        MDMD_feature(n1) = RRR{n1,1};
    end
    
    predicts = {};
    F=MDMD_feature;
    m=k-1;
    C=[];
    for zz=(1+k+m):(l-k-m)
        c=F(zz-k)-(F(zz-k-m)+F(zz-k+m))/2;
        C=[C c];
    end
    
    cmean=mean(C);
    cmax=max(C);
    for p=1:99
        T=cmean+0.01*p*(cmax-cmean);
        T1=T;
        T=ones(l-2*k-2*m,1)*T;
        
        ithframe=find(C>T1);
        ithframe=ithframe+k+m;
        for j=1:num_frames
            predict(j) = 0;
        end
        predict(ithframe)=1;
        
        predicts(p,1) = {p};
        predicts(p,2) = {T1};
        predicts(p,3) = {predict};
    end
    
    save(save_mat_name, 'predicts');
    
    toc
end
