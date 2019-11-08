#主要的流程是
#加载数据->检测一段时间内的事件->追踪事件->预警每个格子的事件
#%%
#通os.chdir(dirname)更改当前工作目录就可以实现成功引入这些包
import os
os.chdir("D:\\EVENTBURST\\mycommunity")
from community_detection import Community_Detecion
from matchevents import Match_Events
from utils import time2timestamp ,timestamp2time
from tqdm import tqdm
import numpy as np
%load_ext autoreload
%autoreload 2
#%%
community_detecion = Community_Detecion()
community_detecion.load_data()#加载数据
#%%
frame_b = "2015/11/10 00:00:00"
frames = []
interval = 3600 *24 #每帧的间隔
num_frames = 6
for i in tqdm(range(num_frames)):
    time_b = timestamp2time(time2timestamp(frame_b)+ (i)*interval)
    time_e = timestamp2time(time2timestamp(time_b)+ interval)
    frame = community_detecion.detect_events(time_b,time_e,i,5)#检测每帧的事件
    frames.append(frame)
#%%
match_events = Match_Events()
ret = match_events.maxweight_match(frames,min_t = 0.2)#min_t指sim的最小值
#%%
print(ret)

# %%
