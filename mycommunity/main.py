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
import gc
gc.collect()
frame_b = "2017/11/01 00:00:00"
print("query_date_begin:{}".format(frame_b))
frames = []
interval = 3600 *24 #每帧的间隔
num_frames = 10
print("query_date_end:{}".format(timestamp2time(time2timestamp(frame_b)+ (num_frames)*interval)))
for i in tqdm(range(num_frames)):
    time_b = timestamp2time(time2timestamp(frame_b)+ (i)*interval)
    time_e = timestamp2time(time2timestamp(time_b)+ interval)
    frame = community_detecion.detect_events(time_b,time_e,i,5)#检测每帧的事件
    frames.append(frame)
#%%
match_events = Match_Events()
ret = match_events.maxweight_match(frames,matrix_t = 0.7,events_t = 0.5)#min_t指sim的最小值
# %%
print(ret.keys())
# %%
print(ret["9_3"])
events_chain = ret['9_3']
docs = []
acc = []
recall = []
for i in events_chain:
    docs.append(i['community_docs'])
    acc.append(i['community_metrics'][0])
    recall.append(i['community_metrics'][1])
# %%
print(ret["9_3"])



# %%
