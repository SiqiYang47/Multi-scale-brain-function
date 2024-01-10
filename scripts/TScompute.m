%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%
%%% Compute the time-series features using hctsa toolbox
%%% fc_path contains the time-series of each brain parcel of each participant
%%% Please cite: Yang Siqi, et al., Macroscale intrinsic Dynamics are associated with Microcircuit Function in Focal and Generalized Epilepsies
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear;clc;

group = 'TLE';
sbj = textread(['/home/sqyang/storage/UESTC/DTI/',group,'.txt'],'%s');
fc_path = ['/mnt/nas/CSC7/Yeolab/Data/UESTC/Func/',group,'_DK68/'];
path = ['/mnt/nas/CSC7/Yeolab/Data/UESTC/Func/hctsa/TS/',group,'/'];

[vertices, label, colortable] = read_annotation('/home/sqyang/storage/UESTC/DTI/template/lh.aparc.annot');
label = colortable.struct_names;
label([1,5],:) = [];
for i=1 : length(label)
    name = label{i};
    hemi = 'lh.';
    new = [hemi,name];
    labels{i}=new;
end
LH = labels';

[vertices, label, colortable] = read_annotation('/home/sqyang/storage/UESTC/DTI/template/rh.aparc.annot');
label = colortable.struct_names;
label([1,5],:) = [];
for i=1 : length(label)
    name = label{i};
    hemi = 'rh.';
    new = [hemi,name];
    labels{i}=new;
end
RH = labels';
labels = [LH;RH];
keywords = labels;
    
    
    
for sub=1 : length(sbj)
    subname = sbj{sub};
    ts = importdata([fc_path,'ROISignals_ROISignal_',subname,'.mat']);
    timeSeriesData = ts'; 
    mkdir([path,subname]);
    cd([path,subname]);
    save([path,subname,'/',subname,'_TS'],'timeSeriesData','labels','keywords');
    
    TS_Init([path,subname,'/',subname,'_TS.mat']);
    TS_Compute(true);
    TS_Normalize('mixedSigmoid',[0,1]);
   
end  















