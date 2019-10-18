# encoding=utf8  
#%%
import networkx as nx
import matplotlib.pyplot as plt
import pyecharts
from pyecharts.charts.basic_charts.graph import Graph
import pandas as pd
import os 
import json
import time
import datetime
from community import community_louvain
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer
#为构图准备数据集
#%%
project_path = "D:/EVENTBURST/data"
file_path = os.path.join(project_path,"mini_data_loc1hot_time1hot.csv")#2015年至2016年举报数据
df = pd.read_csv(file_path)
with open(os.path.join(project_path,'mini_words2id.json'), 'r')as fp:#{key:id}
    words2idx = json.load(fp)
    reversed_words = dict(zip(words2idx.values(),words2idx.keys()))
with open(os.path.join(project_path,'mini_grid_xy2idx.json'), 'r') as fp:#load json
    grid_xy2idx = json.load(fp)
    reversed_locs = dict(zip(grid_xy2idx.values(),grid_xy2idx.keys()))
with open(os.path.join(project_path,'mini_time2idx.json'), 'r') as fp:#load json
    time2idx = json.load(fp)
    reversed_dates = dict(zip(time2idx.values(),time2idx.keys()))
final_embeddings = np.load(os.path.join(project_path,'mini_simple_final_embeddings.npy'),allow_pickle = True)#为了计算方便每个emb的词都进行了归一化长度为1
#%%
def time2timestamp(dt):
    global num_typeerror#使用全局变量
    global num_valueerror
    try:
        timeArray = time.strptime(dt, "%Y/%m/%d %H:%M:%S")#转换成时间戳
        timestamp = time.mktime(timeArray)
        return timestamp
    except TypeError:#其中有1w多条数据没有receive时间
        #print(dt)
        num_typeerror += 1
        return pd.np.nan
    except ValueError:
        num_valueerror += 1
        return pd.np.nan        
def timestamp2time(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return dt
#%%
time_b = '2015/11/10 00:00:00'
time_e = '2015/11/10 23:59:59'
print("查询数据的起始时间是:{},查询的结速时间是:{}".format(time_b,time_e))
q_b = time2timestamp(time_b)
q_e = time2timestamp(time_e)
ret = df[(df['TIMESTAMP'] >q_b) & (df['TIMESTAMP'] < q_e)]
ret = ret.reset_index(drop = True)
m,n = ret.shape
print("查询数据的行数为:{},查询数据的列数为:{}".format(m,n))
keywords = ret['KEY_WORDS']
#%%
#tf-idf的权值
corpus = list(keywords)
vectorizer = CountVectorizer()  
X = vectorizer.fit_transform(corpus)  
word = vectorizer.get_feature_names()  
transformer = TfidfTransformer() 
tfidf = transformer.fit_transform(X).toarray()#tfidf[i][j]是表示第i个文档下标为j的词的权重，所有词都有一个下标
#for i in range(10):
tfidf_word2id ={}
for i,word in enumerate(word):
    tfidf_word2id[word] = i#{词:id}
#%%
ret['EMBEDDINGS'] = None
emb_temp = []
for i in range(m):
    ks = set(keywords[i].split(" "))
    ksemb = np.zeros(128)
    n = 0
    for k in ks:
        try:
            #emb = final_embeddings[words2idx[k]]*tfidf[i][tfidf_word2id[k]]#如果是未登陆词#emb为0,使用tfidf加权计算emb的值
            emb = final_embeddings[words2idx[k]]#不使用tf-idf,而是ebm的均值
            n+=1
        except:
            emb = np.zeros(128)
        ksemb += emb  
    if(n==0):
        ksemb = np.zeros(128)
    else:
        ksemb/=n#每条举报数据的embding是所有关键emb的均值
    emb_temp.append(ksemb)
ret['EMBEDDINGS'] = emb_temp
emb_temp = np.array(emb_temp)
#%%
#构建图的结点集合
nodes = []
for i in range(m):
    nodes.append((i,{'key_words':keywords[i]}))
#构建边的集合
sim = np.matmul(emb_temp,emb_temp.transpose())#计算文档与文档间的相似矩阵
print(sim.shape)
#T值越大划分的社区越多,社区内的类别越细
T = 0.4#相似度的阈值,加了tf_idf权重后,相似性大于T的边减少了,阈值越大则边的数目越少,实验发现T大社区数目增多
print("边相似性的阈值是:{}".format(T))
edges = []
for i in range(m):
    for j in range(i+1,m):
        if(sim[i][j]>T):
            edges.append((i,j,{"weight":sim[i][j]}))
#构图
G = nx.Graph()
G.add_edges_from(edges)
G.add_nodes_from(nodes)
print("图的结点数:{}".format(G.number_of_nodes()))
print("图的边数:{}".format(G.number_of_edges()))
#%%
#nodes = [(1,{'color':'red'}),(2,{'color':'blue'}),(3,{'color':'black'}),(4,{'color':'white'})]#增加结点和结点属性
#edges = [(1,2,{'weight':2}),(1,3,{'weight':2}),(3,2,{'weight':2}),(4,2,{'weight':2}),(1,4,{'weight':2})]
#%%
#绘图
def Draw_Graph(G,save_path):#利用pyecharts绘图
    #G ：要绘制的图
    #save_path : 绘制图的存储位置
    print("图的结点数:{}".format(G.number_of_nodes()))
    print("图的边数:{}".format(G.number_of_edges()))
    r_nodes = [{"name":"","value":0,"symbolSize":5} for i in range(G.number_of_nodes())]
    for i,name in enumerate(G.nodes()):
	    r_nodes[i]["name"] = name
	    r_nodes[i]["value"] = G.degree()[name]#度数可以衡量该结点的重要程度
	    r_nodes[i]["symbolSize"] = G.degree()[name]/10#圆的大小
    r_links = [{"source":"","target":""} for i in range(G.number_of_edges())]
    for i,(u,v) in enumerate(G.edges()):
        r_links[i]["source"] = u
        r_links[i]["target"] = v
        r_links[i]["value"] = G[u][v]["weight"]
    graph = Graph()
    graph.add("",r_nodes,r_links)
    print("Graph begin to Render")
    graph.render(save_path)
#important_nodes = [node for node in G.nodes() if G.degree()[node]>=20]
#G_sub = G.subgraph(important_nodes).copy()
#Draw_Graph(G_sub,'./mycommunity/test.html')

#%%
def Draw_Graph_WithNx(G,alpha,node_scale,figsize):
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor('white')
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_size=[node_scale for x in G.nodes()])
    nx.draw_networkx_edges(G,pos,alpha=alpha)
    nx.draw_networkx_labels(G,pos)
    plt.savefig("./Graph.jpg")
    plt.axis("off")
    plt.show()
#%%
#important_nodes = [node for node in G.nodes() if G.degree()[node]>=100]
#G_sub = G.subgraph(important_nodes).copy()
#Draw_Graph_WithNx(G_sub,alpha=0.5,node_scale=5,figsize=(12,9))
#%%                                   
#python-louvain
partition = community_louvain.best_partition(G) #Louvain算法划分社区,返回的是一个dict,key是文档id value是文档所属社区,可见如果边过多计算时间慢
comm_dict = defaultdict(list)
for doc in partition:
    comm_dict[partition[doc]].append(doc)#[{O:[node1,...,node2]}] {'社区id':"文档list"}
num_comm = len(comm_dict)
print("社区数目为:{}".format(num_comm))
#%%
def Draw_Community(comm,comm_dict,isdraw = False):
    G_comm = G.subgraph(comm_dict[comm]).copy()
    if(isdraw):
        Draw_Graph_WithNx(G_comm,alpha=0.1,node_scale=1,figsize=(16,12))
    reversed(sorted(comm_dict[comm],key=G.degree))#按结点的度排序
    community_member = comm_dict[comm]
    num = len(community_member)
    print("community {} , 元素个数{} , 内容:".format(str(comm),str(num)))
    if num>=10:
        num=10
    for i in range(num):
        print(keywords[community_member[i]])
    #print("社区元素降序:")
    #print("community {}: {}".format(str(comm)," ".join(map(str,reversed(sorted(comm_dict[comm],key=G.degree))))))
    #print("社区元素升序:")
    #print("community {}: {}".format(str(comm)," ".join(map(str,sorted(comm_dict[comm],key=G.degree)))))
#%%
comm_dict = dict(sorted(comm_dict.items(), key=lambda d: len(d[1]),reverse = True))#按社区的元素个数排序
rec = 0
for item in comm_dict.items():
    rec+=1
    if(rec>10):break
    Draw_Community(item[0],comm_dict,isdraw = False)
#%%
#保存时间帧community于一array中[{}]
#{"community_id":社区划分后的id,"community_member":[社区成员],"member_degree":[成员的度数],"member_emb":[成员的embedding],"member_content":["社区内容"]}
ret = []
for item in comm_dict.items():
    if(len(item[1])<4):#社区内数目至少要4条
        continue
    community_temp = {"community_id":-1,"community_member":[],"member_degree":[],"member_emb":[],"member_content":[]}
    community_temp["community_id"] = item[0]
    community_temp["community_member"] = item[1]
    degree_temp = []
    for m in item[1]:
        degree_temp.append(G.degree()[m])
    community_temp["member_degree"] = degree_temp
    community_temp["member_emb"] = emb_temp[item[1]]
    community_temp["member_content"] = keywords[item[1][:4]]
    ret.append(community_temp)
date = time_b.split(" ")[0].split("/")[-1]
np.save(str(date)+".npy",np.array(ret))
#%%
#np.save(time_b+" "+time_e+".npy",np.array(ret))

#目前来说是T=0.4 用一天的数据进行事件检测效果会好点
#主要的问题是相同类别的数据经常会分成多个小类

#%%
