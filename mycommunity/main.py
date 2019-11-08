#主要的流程是
#加载数据->检测一段时间内的事件->追踪事件->预警每个格子的事件
#%%
#通os.chdir(dirname)更改当前工作目录就可以实现成功引入这些包
from community_detection import Community_Detecion
from matchevents import Match_Events
from utils import time2timestamp ,timestamp2time
from tqdm import tqdm
#%%
community_detecion = Community_Detecion()
match_events = Match_Events()
community_detecion.load_data()#加载数据
#%%
time_b = "2015/11/05 00:00:00"
frames = []
interval = 3600 *24 #每帧的间隔
num_frames = 10
for i in tqdm(range(num_frames)):
    time_b = timestamp2time(time2timestamp(time_b)+ (i)*interval)
    time_e = timestamp2time(time2timestamp(time_b)+ (i+1)*interval)
    frame = community_detecion.detect_events(time_b,time_e,i)
    frames.append(frame)
# %%
