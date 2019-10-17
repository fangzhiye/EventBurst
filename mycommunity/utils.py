#辅助类,用来提供辅助功能
import time
import datetime
import pandas as pd

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
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return dt