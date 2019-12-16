#%%
#import mytest
#import community_detection
import numpy as np
import pandas as pd
import collections
import os
from tqdm import tqdm
os.chdir("D:/EVENTBURST/EventBurst_Demo")
from mycommunity.process import Process
from mycommunity.utils import timestamp2time,time2timestamp
#%%
project_path = "D:/EVENTBURST/data"
file_path = os.path.join(project_path,"all_adv_dataseg_loc1hot_time1hot.csv")#2015年至2016年举报数据
df = pd.read_csv(file_path)
df.head()
#%%
keywords = df['KEY_WORDS']
m,n = df.shape
new_keywords = []
for i in range(m):
    new_keywords.append(" ".join(np.array(keywords[i].split(" "))[:-1]))
df['KEY_WORDS'] = new_keywords
#%%
df.to_csv(os.path.join(project_path,"all_adv_dataseg_loc1hot_time1hot.csv"),encoding="utf-8")
# %%
a = np.array([['a','b'],['a']])
print(collections.Counter(a.flatten()))
# %%
a = np.array([['a','b'],['a']])
print(a.flatten())
# %%
keywords = np.array([['1 2 3 4','1 2 3 41'],['2 4 5 6']])
comm_words = [word for keyword in keywords for word in keyword]
print(comm_words)

# %%
myprocess = Process()
frame_b = "2015/05/01 00:00:00" #至2018年7月
interval = 3600*24 #每天
num_frames = 14#两周
res = []
top_k = 3
begin_weeks = 0
end_weeks = 164
for i in tqdm(range(begin_weeks,end_weeks)):
    frame_b_query=timestamp2time(time2timestamp(frame_b)+i*7*interval)
    frames = myprocess.detect(frame_b_query,interval,num_frames)#查询间隔为两周
    chains = myprocess.match(frames)
    bursty = myprocess.preprocess_chains(chains)
    rec = 0
    for k,v in bursty.items():
        #top_k += 1
        #if(rec>top_k):
            #break
        res.append((frame_b_query,k,v))
res = sorted(res,key=lambda item: item[-1],reverse=True)
res = np.array(res)
print(res)
np.save("bursty_events"+str(begin_weeks)+"-"+str(end_weeks)+".npy",res)
# %%
res = np.load("bursty_events.npy")
print(res[:20])

# %%
frame_b = "2015/05/01 00:00:00"
frame_e = "2018/07/01 00:00:00"
num_week = (time2timestamp(frame_b)-time2timestamp(frame_e))/(7*24*3600)
print(num_week)

# %%
