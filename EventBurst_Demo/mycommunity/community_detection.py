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
from sklearn import metrics
import collections
from .utils import time2timestamp ,timestamp2time#这里指从当前包引入utils
#为构图准备数据集
#%%
#使用mini数据
'''
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
'''

#%%
#该类的功能就是检测一段时间内的事件
class Community_Detecion:
    def __init__(self):
        pass
    def load_data(self):
        #为了简单起见在构造这个实例的时候就加载数据
        project_path = "D:/EVENTBURST/data"
        file_path = os.path.join(project_path,"all_adv_dataseg_loc1hot_time1hot.csv")#2015年至2016年举报数据
        self.df = pd.read_csv(file_path)
        with open(os.path.join(project_path,'all_words2id.json'), 'r')as fp:#{key:id}
            self.words2idx = json.load(fp)
            self.reversed_words = dict(zip(self.words2idx.values(),self.words2idx.keys()))
        with open(os.path.join(project_path,'all_adv_grid_xy2idx.json'), 'r') as fp:#load json
            self.grid_xy2idx = json.load(fp)
            self.reversed_locs = dict(zip(self.grid_xy2idx.values(),self.grid_xy2idx.keys()))
        with open(os.path.join(project_path,'all_adv_time2idx.json'), 'r') as fp:#load json
            self.time2idx = json.load(fp)
            self.reversed_dates = dict(zip(self.time2idx.values(),self.time2idx.keys()))
        self.final_embeddings = np.load(os.path.join(project_path,'all_emb_word2vec_s128.npy'),allow_pickle = True)#为了计算方便每个emb的词都进行了归一化长度为1
        self.get_labels()#获得文档的labels
#%%
    def get_labels(self):
        types = set(self.df['TYPE'])#确定labels的时候如果仅二级、三级以最后一级为label,如果四级以第三级为label
        self.labels_dict = {} #{label:idx}是整个文件的所有label,每个label给个idx
        for idx,key in enumerate(types):
            key_list = key.split("-")
            if(len(key_list)>3):
                key = key_list[2]
            else:
                key = key_list[-1]
            if(key not in self.labels_dict.keys()):
                self.labels_dict[key] = idx
        print("number of types : {}".format(len(self.labels_dict)))
        self.rev_labels_dict = {}
        for key,value in self.labels_dict.items():
            self.rev_labels_dict[value] = key
#%%
    def get_querydata(self,time_b, time_e):
        #time_b = '2016/07/20 00:00:00'
        #time_e = '2016/07/20 23:59:59'
        print("查询数据的起始时间是:{},查询的结速时间是:{}".format(time_b,time_e))
        q_b = time2timestamp(time_b)
        q_e = time2timestamp(time_e)
        ret_df = self.df[(self.df['TIMESTAMP'] >q_b) & (self.df['TIMESTAMP'] < q_e)]

        ret_df = ret_df.reset_index(drop = True)
        m,n = ret_df.shape
        print("查询数据的行数为:{},查询数据的列数为:{}".format(m,n))
        return ret_df
#%%
#tf-idf的权值
    def cal_tfidf(self,keywords):   
    #输入keywords返回每个word的权重    
        corpus = list(keywords)
        vectorizer = CountVectorizer()  
        X = vectorizer.fit_transform(corpus)  
        word = vectorizer.get_feature_names()  
        transformer = TfidfTransformer() 
        tfidf = transformer.fit_transform(X).toarray()#tfidf[i][j]是表示第i个文档下标为j的词的权重，所有词都有一个下标
        tfidf_word2id ={}
        for i,word in enumerate(word):
            tfidf_word2id[word] = i#{词:id}
        return tfidf, tfidf_word2id
#%%
#通过emb的方式计算每条举报数据的emb均值或tf*idf 加权计算emb
    def make_docemb(self,ret_df):
        m,n = ret_df.shape
        keywords = ret_df['KEY_WORDS']
        emb_temp = []
        for i in range(m):
            ks = keywords[i].split(" ")
            ksemb = np.zeros(128)
            n = 0
            for k in ks:
                try:
                    #emb = final_embeddings[words2idx[k]]*tfidf[i][tfidf_word2id[k]]#如果是未登陆词#emb为0,使用tfidf加权计算emb的值
                    emb = self.final_embeddings[self.words2idx[k]]#不使用tf-idf,而是ebm的均值
                    n+=1
                except:
                    emb = np.zeros(128)
                ksemb += emb  
            if(n!=0):
                ksemb/=n#每条举报数据的embding是所有关键emb的均值
            emb_temp.append(ksemb)
        emb_temp = np.array(emb_temp)
        emb_temp = [vec/np.linalg.norm(vec) for vec in emb_temp]
        emb_temp = np.array(emb_temp)#维度低点好像同一内容相似度更高
        return emb_temp
    #%%
    #通过实体的共现性 如出现为1不出现为0 或累计实体出现频次计算相似性,可见emb的均值效果好
    '''
    num_words = len(words2idx)
    emb_temp = np.zeros(shape=(m,num_words),dtype = np.int8)
    for i in range(m):
        #ks = set(keywords[i].split(" "))#关键词集合
        ks = keywords[i].split(" ")
        for k in ks:
            try:
                idx = words2idx[k]
                emb_temp[i][idx]+=1
            except:
                pass
    emb_temp = np.array([vec/np.linalg.norm(vec) for vec in emb_temp])
    '''
    #维度低点好像同一内容相似度更高
    #%%
    #构建图的结点集合
    def make_graph(self,ret_df,emb_temp):
        m,n = ret_df.shape
        keywords = ret_df['KEY_WORDS']
        nodes = []
        for i in range(m):
            nodes.append((i,{'key_words':keywords[i]}))
        #构建边的集合
        sim = np.matmul(emb_temp,emb_temp.transpose())#计算文档与文档间的相似矩阵
        #print(sim.shape)
        #T值越大划分的社区越多,社区内的类别越细
        T = 0.8#相似度的阈值,加了tf_idf权重后,相似性大于T的边减少了,阈值越大则边的数目越少,实验发现T大社区数目增多
        #T越大 边越小 社区越多 社区内的类别也更准确
        #print("边相似性的阈值是:{}".format(T))
        edges = []
        for i in range(m):
            for j in range(i,m):
                if(sim[i][j]>T):
                    edges.append((i,j,{"weight":sim[i][j]}))
        #构图
        G = nx.Graph()
        G.add_edges_from(edges)
        G.add_nodes_from(nodes)
        #print("图的结点数:{}".format(G.number_of_nodes()))
        #print("图的边数:{}".format(G.number_of_edges()))
        return G
    #%%
    #nodes = [(1,{'color':'red'}),(2,{'color':'blue'}),(3,{'color':'black'}),(4,{'color':'white'})]#增加结点和结点属性
    #edges = [(1,2,{'weight':2}),(1,3,{'weight':2}),(3,2,{'weight':2}),(4,2,{'weight':2}),(1,4,{'weight':2})]
    #%%
    #绘图
    def Draw_Graph(self,G,save_path):#利用pyecharts绘图
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
    def Draw_Graph_WithNx(self,G,alpha,node_scale,figsize):
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
    def Eva_Metric(self,labels_true, labels_pred):
        #计算聚类的评介指标
        #labels 以样本的二级或三级标题为labels
        #preds 以聚类后类里占多数样本的标签为聚类后的labels
        rand_score = metrics.adjusted_rand_score(labels_true, labels_pred)#兰德系数[-1,1]随机聚类的话发现系数接近于0
        info_score = metrics.adjusted_mutual_info_score(labels_true, labels_pred)#互信息[-1,1]
        v_measure_score = metrics.v_measure_score(labels_true, labels_pred)#同质性、完整性的调合
        mallows_score = metrics.fowlkes_mallows_score(labels_true, labels_pred)#fowlkes_score   
        return (rand_score,info_score,v_measure_score,mallows_score)

    #python-louvain
    def getRealDocs(self,keywords):
        #keywords = ret_df['KEY_WORDS']
        real_doc = 0
        for i in range(len(keywords)):
            ks = keywords[i].split(" ")
            if("漏雨" in ks or "漏水" in ks or "积水" in ks or "排水" in ks):
                real_doc+=1
        return real_doc


    def graph_partition(self,G,ret_df):
        m,n = ret_df.shape
        keywords = ret_df['KEY_WORDS']
        partition = community_louvain.best_partition(G,resolution = 2) #Louvain算法划分社区,返回的是一个dict,key是文档id value是文档所属社区,可见如果边过多计算时间慢
        modularity = community_louvain.modularity(partition,G)
        #print("社区划分的模块度是:{}".format(modularity))
        #resolution 控制社区内数目的大小,越小社区数目越小,resolution可以让供热问题聚类为一类
        comm_dict = defaultdict(list)
        for doc in partition:
            comm_dict[partition[doc]].append(doc)#[{O:[node1,...,node2]}] {'社区id':"文档list"}
        num_comm = len(comm_dict)
        #print("社区数目为:{}".format(num_comm))

        self.labels_true = np.empty(shape=[m])#各条举报数据的label GT
        labels_pred = np.empty(shape=[m])#以同一community中多数的label为这一community的label
        ret_types = list(ret_df['TYPE'])
        for i,d_type in enumerate(ret_types):
            key_list = d_type.split("-")
            if(len(key_list)>3):
                key = key_list[2]
            else:
                key = key_list[-1]
            idx = self.labels_dict[key]
            self.labels_true[i] = idx
        self.labels_true = np.array(self.labels_true)

        '''
        #其实对于兰德系数和互信息并不要求给聚类的元素打label,而只要求他们原本是同一个类别现在聚成同一个簇就好了
        for com_id,com_members in comm_dict.items():
            members_labes = labels_true[com_members]
            com_label = collections.Counter(members_labes).most_common()[0][0]#聚类后聚类id如何和参考id 匹配
            #上面的方法只能说相同的类别容易聚成一个类别，但比如商品质量就聚成了很多个类别？？
            labels_pred[com_members] = com_label
            print("社区的id:{}".format(com_id))
            print("社区的类别:{}".format(rev_labels_dict[com_label]))
        '''
        for com_id,com_members in comm_dict.items():
            labels_pred[com_members] = np.random.randint(0,num_comm)#
            labels_pred[com_members] = com_id#同一个社区的文档预测的是同一个id

        scores = self.Eva_Metric(self.labels_true,labels_pred)
        print(self.getRealDocs(list(keywords)))
        #print(scores)
        return comm_dict,scores 
#%%
    def get_commmetrics(self,comm_members):
        #给定一个社区的成员计算acc recall and f1-score
        members_labels = self.labels_true[comm_members]#获得该社区每个成员的label
        comm_label = collections.Counter(members_labels).most_common()[0][0]#聚类成员最多的label为该社区的label
        acc = collections.Counter(members_labels).most_common()[0][1]/len(comm_members)
        recall = collections.Counter(members_labels).most_common()[0][1]/collections.Counter(self.labels_true)[comm_label]
        f1_score = 2*acc*recall/(acc+recall)
        return [acc,recall,f1_score]
#%%
    def Draw_Community(self,comm,keywords,G,comm_dict,isdraw = False):
        G_comm = G.subgraph(comm_dict[comm]).copy()
        if(isdraw):
            self.Draw_Graph_WithNx(G_comm,alpha=0.1,node_scale=1,figsize=(16,12))
        reversed(sorted(comm_dict[comm],key=G.degree))#按结点的度排序
        community_member = comm_dict[comm]
        num = len(community_member)
        #print("community {} , 元素个数{} , 内容:".format(str(comm),str(num)))
        if num>=5:
            num=5
        #for i in range(num):
            #print(keywords[community_member[i]])
        #print("社区元素降序:")
        #print("community {}: {}".format(str(comm)," ".join(map(str,reversed(sorted(comm_dict[comm],key=G.degree))))))
    #print("社区元素升序:")
    #print("community {}: {}".format(str(comm)," ".join(map(str,sorted(comm_dict[comm],key=G.degree)))))
#%%
    def show_events(self,ret_df,comm_dict,G):
        m,n = ret_df.shape
        keywords = ret_df['KEY_WORDS']
        comm_dict = dict(sorted(comm_dict.items(), key=lambda d: len(d[1]),reverse = True))#按社区的元素个数排序
        rec = 0
        for item in comm_dict.items():
            rec+=1
            if(rec>5):break
            self.Draw_Community(item[0],keywords,G,comm_dict,isdraw = False)
#%%
#保存发现的社区,保存时间帧community于一array中[{}]
#{"community_id":社区划分后的id,"community_member":[社区成员],"member_degree":[成员的度数],"member_emb":[成员的embedding],"member_content":["社区内容"]}
    def get_events(self,ret_df,comm_dict,emb_temp,G,frame_id,min_docs = 4):
        m,n = ret_df.shape
        keywords = np.array((ret_df['KEY_WORDS']))
        types = np.array((ret_df['TYPE']))
        dates = np.array((ret_df['DATE']))
        contents = np.array(ret_df['CONTENT'])
        lats = np.array(ret_df['LATITUDE'])
        lons = np.array(ret_df['LONGITUDE'])
        regions = np.array(ret_df['REGION'])
        ret = []
        #print("类别数目是:{}".format(len(set(types))))
        for item in comm_dict.items():
            #key 是com id
            if(len(item[1])<min_docs):#社区内数目至少要2条
                continue
            community_temp = {"community_id":item[0],"frame_id":frame_id,"community_metrics":[],"community_member":item[1],"member_degree":[],"member_emb":[],"member_content":[]}#因该增加frame_id 记录该事件是在第几帧
            degree_temp = []
            for m in item[1]:
                degree_temp.append(G.degree()[m])
            community_temp["member_degree"] = degree_temp
            community_temp["member_emb"] = emb_temp[item[1]]#member的emb
            community_temp["community_metrics"]=self.get_commmetrics(item[1])
            community_temp["member_content"] = keywords[item[1][:4]]#在这获得检测到的事件内容
            community_temp['community_types'] = types[item[1]]
            community_temp['community_dates'] = dates[item[1]]
            community_temp['community_lats'] = lats[item[1]]
            community_temp['community_lons'] = lons[item[1]]
            community_temp['community_keywords'] = keywords[item[1]]#该comm里每条举报的keywords
            community_temp['community_regions'] = regions[[item[1]]]
            community_temp['community_contents'] = contents[item[1]]
            ret.append(community_temp)
        return ret
        #date = time_b.split(" ")[0].split("/")[-1]
        #np.save(str(date)+".npy",np.array(ret))
#%%
    def detect_events(self,time_b,time_e,frame_id,min_docs):
        ret_df = self.get_querydata(time_b,time_e)#返回这一段时间内的数据
        emb_temp = self.make_docemb(ret_df)#图每个结点的表示
        G = self.make_graph(ret_df,emb_temp)#构图
        comm_dict,scores = self.graph_partition(G,ret_df)#社区发现
        self.show_events(ret_df,comm_dict,G)
        ret = self.get_events(ret_df,comm_dict,emb_temp,G,frame_id,min_docs)
        ret = np.array(ret)
        return ret #[{events1},{events2},{events3}...,{}]
        #keywords = ret_df['KEY_WORDS']
#%%
#应设计成一个类的形式Community_Detection
#类的主要功能是输入一个起始时间和结束时间可以返回这段时间内的所有事件