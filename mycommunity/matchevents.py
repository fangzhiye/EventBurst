#%%
from scipy.optimize import linear_sum_assignment
import numpy as np
'''
This function can also solve a generalization of the classic assignment problem where the cost matrix is rectangular. 
If it has more rows than columns, then not every row needs to be assigned to a column, and vice versa.(反之亦然)
#即如果行多则列的每个顶点都会匹配，如果列多则行的每个顶点都会匹配
#我们需要的是最大权值和匹配
'''
#%%
#是一array array里的元素是[{},{},{}]
#{"community_id":社区划分后的id,"community_member":[社区成员],"member_degree":[成员的度数],"member_emb":[成员的embedding],"member_content":["社区内容"]}
#frames = []
#ret = {} #{frame_id + commid : [{comm1},{comm2},...]}
#for i in range(10,16):
    #frames.append(np.load("./"+str(i)+".npy",allow_pickle=True))
#left_frame = np.load("./14.npy", allow_pickle=True)
#right_frame = np.load("./15.npy",allow_pickle=True)
class Match_Events:
    def __init__(self,embeddings,words2idx):
        self.ret = {}
        self.embeddings = embeddings
        self.words2idx = words2idx
        print("class match events")
        pass
    def get_commemb(self,frame):
        embs_frame = []
        '''
        for comm in frame:
            degree = np.array(comm['member_degree'])
            emb = comm['member_emb']
            all_degree = sum(degree)
            degree = degree / all_degree
            w = np.expand_dims(degree,axis = 1)
            emb *= w #按度数加权
            #emb /= len(degree) #均值
            embs.append(np.sum(emb,axis=0))#embe是事件里每条举报数据度数的加权和
        '''
        for comm in frame:#所有关键词的均值
            embs = np.zeros(128)
            keywords = np.array(comm['community_keywords'])#[['','','']]每个元素都是一个comm
            comm_words = []
            for keyword in keywords:
                for i in keyword.split(" "):
                    comm_words.append(i)
            comm_words = comm_words#不要set 应该是按词频
            n=0
            for word in comm_words:
                try:
                    emb = self.embeddings[self.words2idx[word]]
                    n+=1
                except:
                    emb = np.zeros(128)
                embs+=emb
            if(n!=0):
                embs/=n
            embs_frame.append(embs)
        return np.array(embs_frame)

    def get_weight_commemb(self,left_frame,right_frame):

        for comm in left_frame:
            pass
            #每条doc都是一n维的0,1向量 每个维度出现这个词为1否则为0
            #两条文本都出现这个词的话权重比另一个词高
            #如doc1 [0 0 1 1 0 1]
            #  doc2 [0 1 1 0 1 1]
            # weight[1 1 2 1 1 2]即如果两doc都有该词权重为2 否则为1
            # 小蓝单车 退押金
            # 小蓝单车 退款

    def match_frames(self,left_frame,right_frame,frame_id,matrix_t=0.2,events_t = 0.8):#前一帧为left_fram,后一帧为right_fram
        #T为相似度的阈值
        #frame_id 记录left是第几frame
        #
        left_embs = self.get_commemb(left_frame)
        #print(left_embs)
        right_embs = self.get_commemb(right_frame)
        left_embs = np.array([vec/np.linalg.norm(vec) for vec in left_embs])#归一化比较相似度
        right_embs = np.array([vec/np.linalg.norm(vec) for vec in right_embs])
        l = len(left_frame)
        r = len(right_frame)
        print("left frame communities : {}".format(l))
        print("right frame communities : {}".format(r))
        #如果用cos计算sim 都要归一化
        sim = np.matmul(left_embs,right_embs.transpose())#如果行数小于列数则每行都会匹配到,否则每列都会匹配到
        for i in range(l):
            for j in range(r):
                if(sim[i][j]<matrix_t):sim[i][j]=0
        row_ind, col_ind = linear_sum_assignment(sim*-1)#最大权值二部图匹配所有要*-号
        print(row_ind)
        print(col_ind)
        print(sim[row_ind, col_ind].sum())#因原算法是最小权值匹配所以要乘-1
        match_left = left_frame[row_ind]#如果是相同坐标表示match_left ith元素与match_left ith元素匹配
        match_right = right_frame[col_ind]
        for i in range(len(row_ind)):
            comm_left = {}
            comm_right = {}
            print("left 的id是:{},举报数目是:{},内容是:".format(match_left[i]["community_id"],len(match_left[i]["member_degree"])))
            print(match_left[i]["member_content"])
            comm_left["community_docs"] = len(match_left[i]["member_degree"])
            comm_left["community_content"] = match_left[i]["member_content"]
            comm_left["community_metrics"] = match_left[i]["community_metrics"]
            comm_left["community_types"] = match_left[i]["community_types"]
            comm_left["community_frameid"] = frame_id
            print("匹配的是：")
            print("right 的id是:{},举报数目是:{},内容是:".format(match_right[i]["community_id"],len(match_right[i]["member_degree"])))
            print(match_right[i]["member_content"])
            comm_right["community_docs"] = len(match_right[i]["member_degree"])
            comm_right["community_content"] = match_right[i]["member_content"]
            comm_right["community_metrics"] = match_right[i]["community_metrics"]
            comm_right["community_types"] = match_right[i]["community_types"]
            comm_right["community_frameid"] = frame_id+1
            print("相似度为:{}".format(sim[row_ind[i]][col_ind[i]]))#如果相似度很低则不能匹配
            print("<%%%%%%%%%%%%%%%%%%%>")
            old_key = str(frame_id)+"_"+str(match_left[i]["community_id"])
            new_key = str(frame_id+1)+"_"+str(match_right[i]["community_id"])#匹配为p-q,其中q为key，事件链的终点
            if(sim[row_ind[i]][col_ind[i]] < events_t):#如果事件链间事件的相似性少于阈值则是旧事件的结束或新事件的开始
                if(old_key not in self.ret.keys()):#新事件的开始
                    self.ret[new_key] = []
                    self.ret[old_key] = []
                    self.ret[old_key].append(comm_left) #分别为一个事件结束和一新事件的开始
                    self.ret[new_key].append(comm_right)
                else:
                    self.ret[new_key] = []
                    self.ret[new_key].append(comm_right)
            else:
                if(old_key not in self.ret.keys()):#新事件的开始
                    self.ret[new_key] = []
                    self.ret[new_key].append(comm_left)
                    self.ret[new_key].append(comm_right)
                else:#匹配到旧事件
                    self.ret[old_key].append(comm_right)
                    self.ret[new_key] = self.ret.pop(old_key)
        #每个key都是一事件链,key值是事件链的 "frame_commid"

    def maxweight_match(self,frames,matrix_t,events_t ):
        num_frames = len(frames)
        #key为"frame_id + endcomm_id":[{},{},{},"每个元素为事件"]
        for i in range(num_frames-1):
            self.match_frames(frames[i],frames[i+1],i,matrix_t,events_t)
            print("############ new match begin #############")
        return self.ret
#%%
#每个.py文件其实都是一个模块,python在运行前会先在当前目录、PYTHONPATH、默认目录下搜索模块