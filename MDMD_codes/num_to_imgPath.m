function [ imgPath ] = num_to_imgPath(dataset, images_path, num)

    imPath = '';
    for j=1:length(images_path)
        imPath = [imPath, images_path{j}];
    end


    if strcmp(dataset, 'ME2')
        imgPath = char([imPath, '/img', num2str(sprintf('%03d',num)), '.jpg']);
        
    elseif strcmp(dataset, 'SAMM')
        num = num - 1;
        imgPath = char([imPath, '/', images_path{length(images_path)-2}, '_', num2str(sprintf('%05d',num)), '.jpg']);
        if ~exist(imgPath, 'file')
            imgPath = char([imPath, '/', images_path{length(images_path)-2}, '_', num2str(sprintf('%04d',num)), '.jpg']);
        end
        
    elseif strcmp(dataset, 'SAMM_MEGC')
        imgPath = char([ imPath, '/', images_path{3}, '_', images_path{5}, '_', num2str(sprintf('%05d',num)), '.jpg']);
        if ~exist(imgPath, 'file')
            imgPath = char([ imPath, '/', images_path{3}, '_', images_path{5}, '_', num2str(sprintf('%04d',num)), '.jpg']);
        end
    end

end
