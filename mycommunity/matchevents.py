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
#ret = {}
#for i in range(10,16):
    #frames.append(np.load("./"+str(i)+".npy",allow_pickle=True))
#left_frame = np.load("./14.npy", allow_pickle=True)
#right_frame = np.load("./15.npy",allow_pickle=True)
class Match_Events:
    def __init__(self):
        self.ret = {}
        pass
    def get_commemb(self,frame):
        embs = []
        for comm in frame:
            degree = np.array(comm['member_degree'])
            emb = comm['member_emb']
            all_degree = sum(degree)
            degree = degree / all_degree
            w = np.expand_dims(degree,axis = 1)
            emb *= w
            embs.append(np.sum(emb,axis=0))
        return np.array(embs)

    def match_frames(self,left_frame,right_frame,frame_id,T=0.01):#前一帧为left_fram,后一帧为right_fram
        #T为相似度的阈值
        #frame_id 记录left是第几frame
        left_embs = self.get_commemb(left_frame)
        right_embs = self.get_commemb(right_frame)
        l = len(left_frame)
        r = len(right_frame)
        print("left frame communities : {}".format(l))
        print("right frame communities : {}".format(r))
        sim = np.matmul(left_embs,right_embs.transpose())#如果行数小于列数则每行都会匹配到,否则每列都会匹配到
        for i in range(l):
            for j in range(r):
                if(sim[i][j]<T):sim[i][j]=0
        row_ind, col_ind = linear_sum_assignment(sim*-1)
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
            comm_left["community_id"] = str(frame_id)+"_"+str(match_left[i]["community_id"])
            comm_left["community_content"] = match_left[i]["member_content"]
            comm_left["community_docs"] = len(match_left[i]["member_degree"])
            print("匹配的是：")
            print("right 的id是:{},举报数目是:{},内容是:".format(match_left[i]["community_id"],len(match_right[i]["member_degree"])))
            print(match_right[i]["member_content"])
            comm_right["community_id"] = str(frame_id+1)+"_"+str(match_right[i]["community_id"])
            comm_right["community_content"] = match_right[i]["member_content"]
            comm_right["community_docs"] = len(match_right[i]["member_degree"])
            print("相似度为:{}".format(sim[row_ind[i]][col_ind[i]]))#如果相似度很低则不能匹配
            print("<------------------------------->")
            old_key = str(frame_id)+"_"+str(match_left[i]["community_id"])
            new_key = str(frame_id+1)+"_"+str(match_right[i]["community_id"])#匹配为p-q,其中q为key，事件链的终点
            if(old_key not in self.ret.keys()):#新事件的开始
                self.ret[new_key] = []
                self.ret[new_key].append(comm_left)
                self.ret[new_key].append(comm_right)
            else:#匹配到旧事件
                self.ret[old_key].append(comm_right)
                self.ret[new_key] = self.ret.pop(old_key)
#%%
    def match_events(self,frames):
        num_frames = len(frames)
        #key为"frame_id + endcomm_id":[{},{},{},"每个元素为事件"]
        for i in range(num_frames-1):
            self.match_frames(frames[i],frames[i+1],i+10)
            print("############ new match begin #############")
        return self.ret

#构早相似度矩阵
#cost = np.array([[4.5, 1, 3], [2, 0, 5], [3, 2, 2],[9,0,1]]) * -1#



#%%
#每个.py文件其实都是一个模块,python在运行前会先在当前目录、PYTHONPATH、默认目录下搜索模块