%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% Compute the shared time-series features among HC, TLE and GTCS groups
%%% fc_path contains the time-series of each brain parcel of each participant
%%% Please cite: Yang Siqi, et al., Macroscale intrinsic Dynamics are associated with Microcircuit Function in Focal and Generalized Epilepsies
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%  Save TS for each groups (after normalized)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%clear;clc;

group = 'HC';
sbj = textread(['/home/sqyang/storage/UESTC/DTI/',group,'.txt'],'%s');
path = ['/mnt/nas/CSC7/Yeolab/Data/UESTC/Func/hctsa/TS/',group,'/'];
aa(7729,1) = 0;     %% 7729 represented the all features provided by hctsa toolbox
TS(68,7729,length(sbj)) = 0; %% 68 represented the numbers of brain regions

for sub=1 : length(sbj)
    subname = sbj{sub};
    ts = importdata([path,subname,'/HCTSA_N.mat']);
    ope = table2array(ts.Operations(:,1));
    aa(ope) = 1;
    AAA(:,sub) = aa;
    TS(:,ope,sub) = ts.TS_DataMat;
    clear aa ope ts
end

save(['/home/sqyang/storage/UESTC/Func/hctsa/TS/',group,'_index'],'AAA');
save(['/home/sqyang/storage/UESTC/Func/hctsa/TS/',group,'_TS'],'TS');



%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%  ALL index (after normalized)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear;clc;

HC = importdata('/home/sqyang/storage/UESTC/Func/hctsa/TS/HC_index.mat');
IGE = importdata('/home/sqyang/storage/UESTC/Func/hctsa/TS/IGE_index.mat');
TLE = importdata('/home/sqyang/storage/UESTC/Func/hctsa/TS/TLE_index.mat');
AAA = cat(2,HC,IGE,TLE);

for j = 1 : size(AAA,1)
     label = find(AAA(j,:)==1);
     if length(label)< size(AAA,2)
         index(j,:) = 0;
     else index(j,:) = 1;
     end
end

INDEX = find(index==1);
save('/home/sqyang/storage/UESTC/Func/hctsa/TS/ALL_INDEX','INDEX');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%  Shared TS (after normalized)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear;clc;
path_wb_command = '/apps/HCP/workbench-1.5.0/bin_rh_linux64/wb_command';

HC = importdata('/home/sqyang/storage/UESTC/Func/hctsa/TS/HC_TS.mat');
IGE = importdata('/home/sqyang/storage/UESTC/Func/hctsa/TS/IGE_TS.mat');
TLE = importdata('/home/sqyang/storage/UESTC/Func/hctsa/TS/TLE_TS.mat');
TS = cat(3,HC,IGE,TLE);
INDEX = importdata('/home/sqyang/storage/UESTC/Func/hctsa/TS/ALL_INDEX.mat');
G_TS = TS(:,INDEX,:);

HC = G_TS(:,:,1:108);
IGE = G_TS(:,:,109:187);
TLE = G_TS(:,:,188:262);

