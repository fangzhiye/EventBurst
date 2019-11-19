#%%
#import mytest
#import community_detection
import numpy as np
import pandas as pd
import collections
#%%
project_path = "D:/EVENTBURST/data"
file_path = os.path.join(project_path,"all_adv_dataseg_loc1hot_time1hot.csv")#2015年至2016年举报数据
df = pd.read_csv(file_path)
df.head()
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
