#主要的流程是
#加载数据->检测一段时间内的事件->追踪事件->预警每个格子的事件
#%%
#通os.chdir(dirname)更改当前工作目录就可以实现成功引入这些包
import os
import sys
#sys.path.append("D:\\EVENTBURST\\mycommunity")
#sys.path.append('..')
#os.chdir("D:\\EVENTBURST\\mycommunity")
from .community_detection import Community_Detecion
from .matchevents import Match_Events
from .utils import time2timestamp ,timestamp2time
from tqdm import tqdm
import numpy as np
import gc
#%load_ext autoreload
#%autoreload 2
#%%
class Process:
    def __init__(self):
        pass
    #def load_data(self):
        self.community_detecion = Community_Detecion()
        self.community_detecion.load_data()#加载数据
        print("load data successfully")
#%%
    def detect(self,frame_b,interval,num_frames):
        gc.collect()
        #frame_b = "2016/07/10 00:00:00"
        print("query_date_begin:{}".format(frame_b))
        frames = []
        #interval = 3600 *24 #每帧的间隔
        #num_frames = 10
        print("query_date_end:{}".format(timestamp2time(time2timestamp(frame_b)+ (num_frames)*interval)))
        for i in tqdm(range(num_frames)):
            time_b = timestamp2time(time2timestamp(frame_b)+ (i)*interval)
            time_e = timestamp2time(time2timestamp(time_b)+ interval)
            frame = self.community_detecion.detect_events(time_b,time_e,i,5)#检测每帧的事件
            frames.append(frame)#是一二维数组[[{events1},{events2}],[{events1},{events}]]#每个events是一个社区即多个举报数据的集合
        return frames
#%%
    def match(self,frames):
        self.match_events = Match_Events(self.community_detecion.final_embeddings,self.community_detecion.words2idx)
        ret = self.match_events.maxweight_match(frames,matrix_t = 0.7,events_t = 0.7)#min_t指sim的最小值
        return ret
# %%
    def get_metrics(self,ret):
        gc.collect()
        print(ret.keys())
        print(ret["9_0"])
        events_chain = ret['9_0']
        docs = []
        acc = []
        recall = []
        for i in events_chain:
            docs.append(i['community_docs'])
            acc.append(i['community_metrics'][0])
            recall.append(i['community_metrics'][1])
    def preprocess_chains(self,chains,global_event=True):
        #chains : {key[{},{},{}]}
        #global_event : 是全局还是局部事件
        #返回按bursty排序的chain 和一bursty数组
        #局部事件 遍历所有chain,该chain可以根据其doc的pos被分为多条chain
        '''
        对事件链的第一个结点的e的d根据pos map到对应的grid grid[[{key:[{事件1},{事件二}]}],[grid]]
        即对事件链的d分配到map的各grid,如果chain_key+grid_key一样就往链上加增加结果，否则构成新链
        chain_key+grid_key是新链的key
        '''
        #根据bursty程度对key排序然后遍历
        bursty_dict = {}
        new_chains = {}
        for k,v in chains.items():
            temp = []
            chain = v
            for e in chain:
                num_docs = e["community_docs"]
                temp.append(num_docs)
            temp = np.array(temp)
            if(len(temp>1)):
                ave = np.average(temp)
                std = np.std(temp)
                if(std!=0):
                    bursty_dict[k] = (temp[-1]-ave)/std
                else:
                    bursty_dict[k] = 0
            else:
                bursty_dict[k] = 0
        bursty_dict = dict(sorted(bursty_dict.items(), key=lambda d: d[1],reverse=True))#安value排序
        '''
        for k,v in bursty_dict.items():
            new_chains[k] = chains[k]
        '''
        return bursty_dict


