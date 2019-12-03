function feature=MDMD(dataset, imagesPath, l, k, blocks)

feature=cell(l-2*k,1);

parfor zz=k+1:l-k
    image1 = imread(num_to_imgPath(dataset, imagesPath, zz-k));%read Fi-k image
    image2 = imread(num_to_imgPath(dataset, imagesPath, zz));%read Fi image
    image3 = imread(num_to_imgPath(dataset, imagesPath, zz+k));%read Fi+k image
    [u, v] = RLOF_fun(image1, image2,'RLOF');% compte the optical flow between Fi and Fi-k
    [u2, v2] = RLOF_fun(image1, image3,'RLOF');%compte the optical flow between Fi+k and Fi-k
    theta=rad2deg(atan(u./v));
    % seg = cell(rows,cols);
    L = size(image2);
    RRR=zeros(size(blocks,1),4);
    
    %4 directions-----------------------------------------------------------
    rows = blocks(1);
    cols = blocks(1);
    height=floor(L(1)/rows);
    width=floor(L(2)/cols);
    useg = cell(rows,cols);
    vseg = cell(rows,cols);
    u2seg = cell(rows,cols);
    v2seg = cell(rows,cols);
    thetaseg = cell(rows,cols);
    
    Rset=[];
    for row=1:rows
        for col=1:cols
            useg(row,col)= {u((row-1)*height+1:row*height,(col-1)*width+1:col*width,:)};
            vseg(row,col)= {v((row-1)*height+1:row*height,(col-1)*width+1:col*width,:)};
            u2seg(row,col)= {u2((row-1)*height+1:row*height,(col-1)*width+1:col*width,:)};
            v2seg(row,col)= {v2((row-1)*height+1:row*height,(col-1)*width+1:col*width,:)};
            thetaseg(row,col)= {theta((row-1)*height+1:row*height,(col-1) *width+1:col*width,:)};
            
            
            orientation = cell(1,4);
            orientation{1,1}=find(thetaseg{row,col}>=0 & thetaseg{row,col}<90);
            orientation{1,2}=find(thetaseg{row,col}>=90 & thetaseg{row,col}<180);
            orientation{1,3}=find(thetaseg{row,col}>=-180 & thetaseg{row,col}<-90);
            orientation{1,4}=find(thetaseg{row,col}>=-90 & thetaseg{row,col}<0);
            o=zeros(1,4);
            for i=1:4
                o(1,i)=size(orientation{1,i},1);
            end
            [m,i]=max(o);
            
            R=zeros(1,m);
            R2=zeros(1,m);
            for w=1:m
                um=useg{row,col}(orientation{1,i}(w));
                vm=vseg{row,col}(orientation{1,i}(w));
                um2=u2seg{row,col}(orientation{1,i}(w));
                vm2=v2seg{row,col}(orientation{1,i}(w));
                [thetam,rhom] = cart2pol(um,vm);
                [thetam2,rhom2] = cart2pol(um2,vm2);
                R(1,w)=rhom;
                R2(1,w)=rhom2;
            end
            R=R-R2;
            R=sort(R,'descend');
            R=R(1:round(m/3));
            RRmean=mean(R);
            Rset=[Rset RRmean];
        end
    end
    Rset=sort(Rset,'descend');
    Rset=Rset(1:round(rows*cols/3));
    ansf=mean(Rset);
    RRR=ansf;
    
    feature{zz-k,1}=RRR;
    disp(strcat(num2str(zz),'frame is computed.'));
end
