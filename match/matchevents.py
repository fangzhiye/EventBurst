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
left_frame = np.load("./14.npy", allow_pickle=True)
right_frame = np.load("./15.npy",allow_pickle=True)
def get_commemb(frame):
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
left_embs = get_commemb(left_frame)
right_embs = get_commemb(right_frame)
l = len(left_frame)
r = len(right_frame)
print("left frame communities : {}".format(l))
print("right frame communities : {}".format(r))
sim = np.matmul(left_embs,right_embs.transpose())
print(sim.shape)
#%%

#构早相似度矩阵
#cost = np.array([[4.5, 1, 3], [2, 0, 5], [3, 2, 2],[9,0,1]]) * -1#
row_ind, col_ind = linear_sum_assignment(sim*-1)
print(row_ind)
print(col_ind)
print(sim[row_ind, col_ind].sum())#因原算法是最小权值匹配所以要乘-1
match_left = left_frame[row_ind]
match_right = right_frame[col_ind]
for i in range(len(row_ind)):
    print("left 的举报数目是:{},内容是:".format(len(match_left[i]["member_degree"])))
    print(match_left[i]["member_content"])
    print("匹配的是：")
    print("right 的举报数目是:{},内容是:".format(len(match_right[i]["member_degree"])))
    print(match_right[i]["member_content"])
    print("<--------------------------------------------->")
#%%
