#%%
from gensim.models import word2vec
import os
import pandas as pd
import json
import numpy as np
# %%
project_path = "D:/EVENTBURST/data"
file_path = os.path.join(project_path,"all_adv_dataseg_loc1hot_time1hot.csv")#2015年至2016年举报数据
df = pd.read_csv(file_path)
#%%
raw_sentences = list(df["KEY_WORDS"])
print("part data :{}".format(raw_sentences[:5]))
sentences= [s.split(" ") for s in raw_sentences]
model = word2vec.Word2Vec(sentences, min_count=5,size=128,sg = 1,iter = 20)
#emb 的size,iter对结果的影响是什么呢？
#%%
#保存模型
model.save(os.path.join(project_path, "word2vec_s128_it20.model"))
#加载模型
#%%
req_count = 20
for key in model.wv.similar_by_word('积水', topn =50):
    req_count -= 1
    print (key[0], key[1])
    if req_count == 0:
        break
# %%
with open(os.path.join(project_path,'all_words2id.json'), 'r')as fp:#{key:id}
    words2idx = json.load(fp)
num_words = len(words2idx)
final_embeddings = np.empty(shape=[num_words,128])
num_err = 0
for item in words2idx.items():
    key = item[0]#word
    idx = item[1]#id
    try:
        vector = model.wv[key]
    except:
        vector = np.zeros(128)
        num_err+=1
    final_embeddings[idx] = vector
print("all words: {}, num_err: {}".format(num_words,num_err))
# %%
#final_embeddings = [vec/np.linalg.norm(vec) for vec in final_embeddings]#归一化,emb其实不用归一化，最后整个文档的的emb均值因用cos相似度才要归一化
np.save(os.path.join(project_path,"all_emb_word2vec_s128.npy"),final_embeddings)
# %%
