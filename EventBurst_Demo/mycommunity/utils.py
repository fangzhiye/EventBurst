#辅助类,用来提供辅助功能
import time
import datetime
import pandas as pd
import random
num_typeerror = 0
num_valueerror = 0

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
    dt = time.strftime("%Y/%m/%d %H:%M:%S",time_local)
    return dt

def getColor(num_colors=24):
    ret = ["#c23531","#2f4554","#61a0a8","#d48265","#749f83","#ca8622","#bda29a","#6e7074","#546570","#c4ccd3","#f05b72","#ef5b9c","#f47920","#905a3d","#fab27b","#2a5caa","#444693","#726930","#b2d235","#6d8346","#ac6767","#1d953f","#6950a1","#918597","#999933","#FFFFCC","#CC99CC","#996699","#CCCC99","#669999","#996699","#9999CC","#CCCCFF","#CC9966","#666666","#CC9999","#CC9966","#999999","#666666","#CCCC99","#999999","#CCCC99","#333333","#336699","#0099CC","#CCCCCC","#996699","#CCCC99","#666666","#CC9999"]
    if(len(ret)>=num_colors):
        return ret
    for c in range(num_colors):
        color = "#"
        arr = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
        for i in range(6):
            num = random.randint(0,15)
            color += arr[num]
        ret.append(color) 
    #ret.append("rgba(0,0,0,0)") #最后一个颜色是透明
    return ret#返回颜色表

