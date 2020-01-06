from django.shortcuts import render
import numpy as np
import collections
import json
# Create your views here.
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig, SymbolType
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./demo/templates"))

from pyecharts import options as opts
from pyecharts.charts import Page, ThemeRiver, Bar, Map, Geo, Grid, Line, Scatter, Timeline,WordCloud, BMap
from pyecharts.faker import Collector, Faker
from pyecharts.globals import ThemeType
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import os
#import sys
#sys.path.append("..")
from mycommunity.process import Process
from mycommunity.utils import time2timestamp,getColor
#from mycommunity.process import myprocess
#print(sys.path)
from django.http import JsonResponse
process = Process()

def index(request):
    request.encoding='utf-8'
    if 'date_begin' in request.GET and request.GET['date_begin']:
        message = '你搜索的内容为: ' + request.GET['date_begin']
    else:
        message = '你提交了空表单'
    c = (
        Bar()
        .add_xaxis([message, "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    #return render(request, 'clusters/index.html')#render(request,templatesname,content)#content是一dict
    #return HttpResponse(c.render_embed())#.render()会生成html文件
    return HttpResponse(c.render_embed(template_name="simple_chart_test.html"))#render_embed()指渲染包含选项的js代码

def get_bar():
    bar = (
        Bar()
        .add_xaxis(['商家', "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return bar

def get_scatter() -> Scatter:
    #print(Faker.values())
    #Scatter().set_global_opts()
    scatter = (
        Scatter()
        .add_xaxis(['举报时间','经度','维度','举报内容'])
        #.add_yaxis("商家A", Faker.values())
        #.add_yaxis("商家B", Faker.values())
        .set_global_opts(
            #title_opts=opts.TitleOpts(title="Grid-Scatter"),
            legend_opts=opts.LegendOpts(pos_left="20%"),
            yaxis_opts=opts.AxisOpts(is_show=False)
        )
        
    )
    return scatter

def themeriver_formatter(params):
    return "test"

def get_themeriver(data,lengend,num_frames):
    '''
    data = [
        ["2015/11/08", 10, "DQ"],
        ["2015/11/09", 15, "DQ"],
        ["2015/11/10", 35, "DQ"],
        ["2015/11/14", 7, "DQ"],
        ["2015/11/15", 2, "DQ"],
        ["2015/11/16", 17, "DQ"],
        ["2015/11/17", 33, "DQ"],
        ["2015/11/18", 40, "DQ"],
        ["2015/11/19", 32, "DQ"],
        ["2015/11/20", 26, "DQ"],
        ["2015/11/08", 35, "TY"],
        ["2015/11/09", 36, "TY"],
        ["2015/11/10", 37, "TY"],
        ["2015/11/11", 22, "TY"],
        ["2015/11/12", 24, "TY"],
        ["2015/11/13", 26, "TY"],
        ["2015/11/14", 34, "TY"],
        ["2015/11/15", 21, "TY"],
        ["2015/11/16", 18, "TY"],
        ["2015/11/17", 45, "TY"],
        ["2015/11/18", 32, "TY"],
        ["2015/11/19", 35, "TY"],
        ["2015/11/20", 30, "TY"],
        ["2015/11/08", 21, "SS"],
        ["2015/11/09", 25, "SS"],
        ["2015/11/10", 27, "SS"],
        ["2015/11/11", 23, "SS"],
        ["2015/11/12", 24, "SS"],
        ["2015/11/13", 21, "SS"],
        ["2015/11/14", 35, "SS"],
        ["2015/11/15", 39, "SS"],
        ["2015/11/16", 40, "SS"],
        ["2015/11/17", 36, "SS"],
        ["2015/11/18", 33, "SS"],
        ["2015/11/19", 43, "SS"],
        ["2015/11/20", 40, "SS"],
        ["2015/11/14", 7, "QG"],
        ["2015/11/15", 2, "QG"],
        ["2015/11/16", 17, "QG"],
        ["2015/11/17", 33, "QG"],
        ["2015/11/18", 40, "QG"],
        ["2015/11/19", 32, "QG"],
        ["2015/11/20", 26, "QG"],
        ["2015/11/21", 35, "QG"],
        ["2015/11/22", 40, "QG"],
        ["2015/11/23", 32, "QG"],
        ["2015/11/24", 26, "QG"],
        ["2015/11/25", 22, "QG"],
        ["2015/11/08", 10, "SY"],
        ["2015/11/09", 15, "SY"],
        ["2015/11/10", 35, "SY"],
        ["2015/11/11", 38, "SY"],
        ["2015/11/12", 22, "SY"],
        ["2015/11/13", 16, "SY"],
        ["2015/11/14", 7, "SY"],
        ["2015/11/15", 2, "SY"],
        ["2015/11/16", 17, "SY"],
        ["2015/11/17", 33, "SY"],
        ["2015/11/18", 40, "SY"],
        ["2015/11/19", 32, "SY"],
        ["2015/11/20", 26, "SY"],
        ["2015/11/21", 35, "SY"],
        ["2015/11/22", 4, "SY"],
        ["2015/11/23", 32, "SY"],
        ["2015/11/24", 26, "SY"],
        ["2015/11/25", 22, "SY"],
        ["2015/11/08", 10, "DD"],
        ["2015/11/09", 15, "DD"],
        ["2015/11/10", 35, "DD"],
        ["2015/11/11", 38, "DD"],
        ["2015/11/12", 22, "DD"],
        ["2015/11/13", 16, "DD"],
        ["2015/11/14", 7, "DD"],
        ["2015/11/15", 2, "DD"],
        ["2015/11/16", 17, "DD"],
        ["2015/11/17", 33, "DD"],
        ["2015/11/18", 4, "DD"],
        ["2015/11/19", 32, "DD"],
        ["2015/11/20", 26, "DD"],
    ]
    '''
    themeriver = (
        ThemeRiver()
        .add(
            #["DQ", "TY", "SS", "QG", "SY", "DD"],
            lengend,
            data,
            singleaxis_opts=opts.SingleAxisOpts( pos_bottom="50%",min_=1,max_=num_frames),#可以通过调整坐标轴来调整图的位置
            label_opts = opts.LabelOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(formatter="{a}")#不能用 不知道为什么
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="事件链河流图",subtitle="图例按突发性程度降序排序"),
                         #tooltip_opts=opts.TooltipOpts(is_show=True,trigger="item",formatter='{@[0]}'),#formatter目前没效果？？？
                         legend_opts=opts.LegendOpts(type_ = 'scroll',pos_left="5%",orient='vertical',pos_top="55%"))
                        #datazoom_opts=opts.DataZoomOpts())#图例设置
                        
    )
    return themeriver

def get_line(line_data):
    print(Faker.values())
    print(Faker.choose())
    x = line_data['x']
    y = line_data['y']
    line = (
        Line()
        .add_xaxis(x)
        #.add_yaxis("商家A", Faker.values())
        .add_yaxis(
            "举报数目", y,
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
            is_smooth=True
            )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="帧",splitarea_opts=opts.SplitLineOpts(is_show=True),boundary_gap=False),
            yaxis_opts=opts.AxisOpts(
                name="举报数目",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True,    
            ),
            #title_opts=opts.TitleOpts(title="天津政府服务热线数目变化", pos_right="center"),
            legend_opts=opts.LegendOpts(is_show=False),
            #legend_opts=opts.LegendOpts(pos_top="20%"),
            #datazoom_opts=opts.DataZoomOpts(range_start=0,range_end=100),
            #xaxis_opts=opts.AxisOpts(type_="value")#经轴是数值value
            #toolbox_opts=opts.ToolboxOpts(pos_left="right")
        )
        .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    )
    
    return line

def get_bmap(pos) -> BMap:
    BAIDU_AK = "HOTBRAfU1jGcQKHBX15ucKsfZO722eyN"
    #center = (117.20, 39.12)
    c = BMap()
    c.add_schema(
            baidu_ak=BAIDU_AK,
            center=[117.20, 39.12],
            zoom = 10,
            is_roam=False
    )
    sequence = []
    for i in range(len(pos)):
        #print(pos[i])
        c.add_coordinate(pos[i][0],pos[i][2],pos[i][1])
        sequence.append((str(i),5))
    c.add(
        "投诉坐标",#系列名称
        sequence,
        type_="scatter",#"heatmap" 可以切换显示的类型热力图或散点图
        label_opts=opts.LabelOpts(formatter="{b}"),
        symbol_size=4#scatter大小
    )
    #.add("bmap",
        #[{"coord":[117.21, 39.13],"sim":10},{"coord":[117.20, 39.13],"sim":20},{"coord":[117.21, 39.12],"sim":5}],
        #[list(z) for z in zip(Faker.provinces, Faker.values())],#zip将迭代对像打包成元组最后的结果是[['浙江',v1],['广东',v2]]
        #[[117.21, 39.13],[117.20, 39.12],[117.22, 39.10],[117.25, 39.11],[117.19, 39.02],[117.20, 39.12]],
        #type_="heatmap",
        #label_opts=opts.LabelOpts(formatter="{b}"))
    c.set_series_opts(effect_opts=opts.EffectOpts(is_show=True),
                      label_opts=opts.LabelOpts(is_show=False),
                      )
    c.add_control_panel(
        scale_control_opts=opts.BMapScaleControlOpts(),
        navigation_control_opts=opts.BMapNavigationControlOpts(),
        maptype_control_opts=opts.BMapTypeControlOpts())
        #copyright_control_opts=opts.BMapCopyrightTypeOpts(copyright_="我的")
        #geo_location_control_opts=opts.BMapGeoLocationControlOpts()
        #overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),
    #c.set_global_opts(visualmap_opts=opts.VisualMapOpts(pos_left="right"))
    return c

def get_mymap(message) -> Geo:
    pos = (117.20, 39.12)
    tianjing_map = (
         Geo()
        .add_schema(maptype="北京",is_roam=False)
        # 加入自定义的点，格式为
        #.add_coordinate("测试点", pos[0],pos[1])
        #.add(
        #    "测试点",[("测试点", 51)],type_="effectScatter",
        #    label_opts=opts.LabelOpts(formatter="{b}"),
        #)
        #.add_coordinate_json("./demo/coord.json")
        # 为自定义的点添加属性
        #.add("测试点",[("测试点", 51)],type_="effectScatter")
        .add("bmap",
            [list(z) for z in zip(Faker.provinces, Faker.values())],
            type_="heatmap",
            label_opts=opts.LabelOpts(formatter="{b}"))
        #.set_series_opts()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                         effect_opts=opts.EffectOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title=message,pos_right="center"),
                    )
    )
    return tianjing_map
#对事件链按bursty程度排序,并得到其对应的bursty值
def get_wordcloud(words):
    '''
    words = [
    ("Sam S Club", 10000),
    ("Macys", 6181),
    ("Amy Schumer", 4386),
    ("Jurassic World", 4055),
    ("Charter Communications", 2467),
    ("Chick Fil A", 2244),
    ("Planet Fitness", 1868),
    ("Pitch Perfect", 1484),
    ("Express", 1112),
    ("Home", 865),
    ("Johnny Depp", 847),
    ("Lena Dunham", 582),
    ("Lewis Hamilton", 555),
    ("KXAN", 550),
    ("Mary Ellen Mark", 462),
    ("Farrah Abraham", 366),
    ("Rita Ora", 360),
    ("Serena Williams", 282),
    ("NCAA baseball tournament", 273),
    ("Point Break", 265),
    ]
    '''
    wordcloud = (
                WordCloud()
                .add("", words, word_size_range=[1, 100])
                #.set_global_opts(title_opts=opts.TitleOpts(title="事件链词云图"))
                
            )
    return wordcloud

def process_data(frames,chains,bursty_dict,colors_table,lengend_status=None):#所有事件
    #frames[[{event1},{event2}],[{event1},{event2}]]
    #chain{"key":[{event1}->{event2}->{event2}]}
    #lengend_status: 图例被选中的状态
    line_data = {'x':[],'y':[]}#画折线图只要x轴和y轴的数据
    themeriver_data =[]       #[["第i帧数",事件链在第i帧举报数目,"事件链关键词"]]
    themreiver_lengend = []
    wordcloud_data = {}
    pos = []#每条举报数据的位置
    idx = 1
    pos_idx = 0
    numdocs_frame = {}#记录每一帧的举报数目
    for i in range(len(frames)):
        #frame = frames[i]
        line_data['x'].append(str(i+1))#帧的序号,x轴是str类型 从1开始
        '''
        y = 0
        for e in frame:
            y+=len(e["member_degree"])
        line_data['y'].append(y)#每帧的举报数目
        '''
    #print(chains)
    #for k,v in chains.items():
    if(lengend_status):
        lengend_status = list(lengend_status.items())
    for p in range(len(chains)):#p是第p条事件链
        k = list(chains.keys())[p]
        v = chains[k]
        if(lengend_status and lengend_status[p][1]==False):#如果图例是false则不统计了
            #print(lengend_status[p])
            continue
        chain = v#[{},{},{}] ...
        abstract = " "+str(idx)+" "+str(round(bursty_dict[k],2))+" "  #每条事件链的摘要
        idx+=1
        temp = []
        for e in chain:#事件链上的每个结点
            keywords = e["community_keywords"]#array["","",""]
            lats = e["community_lats"]
            lons = e["community_lons"]
            cons = e['community_contents']#举报内容

            for k in keywords:
                for w in k.split(" "):#所有的词
                    temp.append(w)
                    if(w not in wordcloud_data.keys()):
                        wordcloud_data[w] = 1
                    else:
                        wordcloud_data[w]+=1

            for i in range(len(lats)):
                la = lats[i]
                lo = lons[i]
                pos.append((str(pos_idx),la,lo,colors_table[p],cons[i]))
                pos_idx += 1
        C = np.array(collections.Counter(temp).most_common())#[("word":num)]
        if(len(C)<5):#lengend 5个词即可
            e = len(C)
        else:
            e = 5#themeriver 显示25个词
        for i in range(e):
            abstract+=C[i][0]
            abstract+=" "#事件链的摘要
        themreiver_lengend.append(abstract)
        for e in chain:
            frame_id = str(e["community_frameid"]+1)
            if(frame_id not in numdocs_frame.keys()):
                numdocs_frame[frame_id] = e["community_docs"]
            else:
                numdocs_frame[frame_id] += e["community_docs"]
            num_docs = e["community_docs"]
            themeriver_data.append([frame_id,num_docs,abstract])
    #print(themreiver_lengend)
    for i in range(len(frames)):
        key = str(i+1)
        if key in numdocs_frame:
            line_data['y'].append(numdocs_frame[key])
        else:
            line_data['y'].append(0)
    words = list(wordcloud_data.items())
    return line_data,themeriver_data,themreiver_lengend,pos,words

def preprocess_chains(chains,global_event=True):
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
    for k,v in bursty_dict.items():
        new_chains[k] = chains[k]
    return new_chains,bursty_dict

frames = []
chains = []
chainIdx = -1
date_begin_old = ""
date_end_old = ""
timeInterval_old = -1
bursty_dict = {}
colors_table = []

def event_chain_temp(request):
    global frames
    global chains
    global chainIdx
    global date_begin_old
    global date_end_old
    global timeInterval_old
    context={}
    '''
    grid = (
        Grid()
        .add(get_line(), grid_opts=opts.GridOpts(pos_left="55%"))
        .add(get_mymap(), grid_opts=opts.GridOpts(pos_right="50%"))
    )
    '''
    request.encoding='utf-8'
    if(date_begin_old==""):
        date_begin = "2015/11/10"#初始
        date_begin = "2015/11/10 00:00:00"
    if(date_end_old==""):
        date_end = "2015/11/12"
        date_end = "2015/11/12 00:00:00"
    timeInterval = 24
    num_frames = 5
    #如果有查询序号就执行查看event页面
    if 'chainIdx' in request.GET and request.GET['chainIdx']:
        print("bigin to url: chain")
        chainIdx = int(request.GET['chainIdx'])-1#下标从0开始，所以要减一
        return event(request)
    if 'date_begin' in request.GET and request.GET['date_begin']:
        context["last_date_begin"] = request.GET['date_begin']
        date_begin = request.GET['date_begin']+" "+"00:00:00"
        date_begin = date_begin.replace("-","/")
        print("databigin:{}".format(date_begin))
    if 'date_end' in request.GET and request.GET['date_end']:
        context["last_date_end"] = request.GET['date_end']
        date_end = request.GET['date_end']+" "+"00:00:00"
        date_end = date_end.replace("-","/")
        print("dataend:{}".format(date_end))
    #if(date_end="")
    num_frames = int((time2timestamp(date_end)-time2timestamp(date_begin))/(3600*timeInterval))
    print("num_frames:{}".format(num_frames))
    #如果获得经度和维度,就可以在process.detect中删除不在这经度和维度范围内的数据 to do
    if(date_begin_old!=date_begin or date_end_old !=date_end or timeInterval_old!=timeInterval):#如果有一个更新
        frames = process.detect(date_begin,3600*timeInterval,num_frames)
    #line_data = frames
    #不论是全城还是局部事件都要对chain做预处理操作，并且只返回前top20的事件链
        chains = process.match(frames)
    chains,bursty_dict = preprocess_chains(chains)#对chains做一些处理按bursty、glbal/local处理
    date_begin_old = date_begin
    date_end_old = date_end
    timeInterval_old = timeInterval
    #print(chain)
    line_data,themeriver_data,themeriver_lengend, pos,words = process_data(frames,chains,bursty_dict)
    page = Page()#如果要让地图正常显示必须Page里配置为空 
    mymap = get_bmap(pos)
    #mymap = get_mymap(message)
    mymap.chart_id = "bmap_1"#
    wordcloud = get_wordcloud(words)
    wordcloud.chart_id = "wordcloud_1"
    myline = get_line(line_data)
    myline.chart_id = "line_1"
    mythemeriver = get_themeriver(themeriver_data,themeriver_lengend,num_frames)
    mythemeriver.chart_id = "themeriver_1"
    
    # 需要自行调整每个 chart 的 height/width，显示效果在不同的显示器上可能不同
    page.add(mymap)
    page.add(wordcloud)
    page.add(myline)
    
    page.add(mythemeriver)
    page.render(template_name="simple_page_test.html")
    Page.save_resize_html("render.html", cfg_file="./demo/chart_config.json", dest="./demo/templates/my_new_charts.html")
    return render(request,"my_new_charts.html")
    #return HttpResponse(page.render_embed(template_name="simple_page_test.html"))

#只考虑查看单独一个事件的内容
def get_eventmap(message) -> Geo:
    tianjing_map = (
         Geo()
        .add_schema(maptype="天津")
        # 加入自定义的点，格式为
        .add_coordinate("测试点", 117.20, 39.12)
        # 为自定义的点添加属性
        .add("测试点",[("测试点", 51)])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title=message,pos_right="center"),legend_opts=opts.LegendOpts(is_show=False))
    )
    return tianjing_map

'''
def get_eventbmap(message) -> BMap:
    BAIDU_AK = "HOTBRAfU1jGcQKHBX15ucKsfZO722eyN"
    pos = (117.20, 39.12)
    c = (
        BMap()
        .add_schema(
            baidu_ak=BAIDU_AK,
            center=[117.20, 39.12],
            zoom = 10
        )
        .add_coordinate("测试点", pos[0],pos[1])
        .add(
            "测试点",[("测试点", 51)],type_="effectScatter",
            label_opts=opts.LabelOpts(formatter="{b}"),
        )
        .set_series_opts(effect_opts=opts.EffectOpts(is_show=True),
                        label_opts=opts.LabelOpts(is_show=False))
        .add_control_panel(
            scale_control_opts=opts.BMapScaleControlOpts(),
            navigation_control_opts=opts.BMapNavigationControlOpts(),
            maptype_control_opts=opts.BMapTypeControlOpts(),
            #copyright_control_opts=opts.BMapCopyrightTypeOpts(copyright_="我的")
            #geo_location_control_opts=opts.BMapGeoLocationControlOpts()
            #overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),
        )
        #.set_global_opts(title_opts=opts.TitleOpts(title="BMap-基本示例"))
    )
    return c
'''
def get_eventbmap(pos) -> BMap:
    #[(lo,la),(lo,la)]这种格式即可
    BAIDU_AK = "HOTBRAfU1jGcQKHBX15ucKsfZO722eyN"
    center = (117.20, 39.12)
    c = BMap()
    c.add_schema(
            baidu_ak=BAIDU_AK,
            center=[117.20, 39.12],
            zoom = 10,
            is_roam=False,  
    )
    sequence = []
    for i in range(len(pos)):
        c.add_coordinate(str(i),pos[i][0],pos[i][1])#[(posindex,lo,la)]
        sequence.append((str(i),0.1))#这里名字和pos要对应
    c.add(
        "投诉坐标",#系列名称
        sequence,
        type_="scatter",#"heatmap" 可以切换显示的类型热力图或散点图
        label_opts=opts.LabelOpts(formatter="{b}"),
        symbol_size=5
    )
    c.set_series_opts(effect_opts=opts.EffectOpts(is_show=True),
                    label_opts=opts.LabelOpts(is_show=False))
    c.add_control_panel(
        scale_control_opts=opts.BMapScaleControlOpts(),
        navigation_control_opts=opts.BMapNavigationControlOpts(),
        maptype_control_opts=opts.BMapTypeControlOpts())
    #c.set_global_opts(visualmap_opts=opts.VisualMapOpts())
    return c

def get_eventline(line_data):
    print(Faker.values())
    print(Faker.choose())
    x = line_data['x']
    y = line_data['y']
    line = (
        Line()
        .add_xaxis(x)
        #.add_yaxis("商家A", Faker.values())
        .add_yaxis(
            "举报数目", y,
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
            is_smooth=True
            )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="帧数",splitarea_opts=opts.SplitLineOpts(is_show=True), boundary_gap=False),
            yaxis_opts=opts.AxisOpts(
                name="举报数目",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True,
            ),
            #title_opts=opts.TitleOpts(title="天津政府服务热线数目变化", pos_right="center"),
            legend_opts=opts.LegendOpts(is_show=False),
            toolbox_opts=opts.ToolboxOpts(pos_left="right"),
            #legend_opts=opts.LegendOpts(pos_top="20%"),
            datazoom_opts=opts.DataZoomOpts(range_start=0,range_end=100),
            #xaxis_opts=opts.AxisOpts(type_="value")#经轴是数值value
            #toolbox_opts=opts.ToolboxOpts(orient='vertical',pos_right="right")
        )
    .set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5))
    ) 
    return line

def get_eventtable(rows) -> Table:
    table = Table()
    headers = ["序号","日期","举报内容","所属区域","维度","经度"]
    for r in rows:
        c = r[2]
        cl = list(c)
        n_w = len(cl)
        idx = int((n_w-1)/30)#每40个词分行
        if(idx<1):
            continue
        for i in range(idx):
            cl.insert((i+1)*30,"\n")
        r[2] = "".join(cl)
    '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    headers = ["City name", "Area", "Population", "Annual Rainfall"]
    rows = [
        ["Brisbane", 5905, 1857594, 1146.4],
        ["Adelaide", 1295, 1158259, 600.5],
        ["Darwin", 112, 120900, 1714.7],
        ["Hobart", 1357, 205556, 619.5],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
    ]
    '''
    table.add(headers, rows).set_global_opts(
        title_opts=ComponentTitleOpts(title="详细举报数据"),
    )
    return table

def get_wordcloud_line(words,frame_ids)->Line:
    tl = Timeline()
    #print(words)
    '''
    words = [
    ("Sam S Club", 10000),
    ("Macys", 6181),
    ("Amy Schumer", 4386),
    ("Jurassic World", 4055),
    ("Charter Communications", 2467),
    ("Chick Fil A", 2244),
    ("Planet Fitness", 1868),
    ("Pitch Perfect", 1484),
    ("Express", 1112),
    ("Home", 865),
    ("Johnny Depp", 847),
    ("Lena Dunham", 582),
    ("Lewis Hamilton", 555),
    ("KXAN", 550),
    ("Mary Ellen Mark", 462),
    ("Farrah Abraham", 366),
    ("Rita Ora", 360),
    ("Serena Williams", 282),
    ("NCAA baseball tournament", 273),
    ("Point Break", 265),
    ]
    '''
    for i in frame_ids:
        wordcloud = (
            WordCloud()
            .add("", words, word_size_range=[10, 100])
            .set_global_opts(title_opts=opts.TitleOpts(title="事件链词云图"))
            
        )
        tl.add(wordcloud, "{}帧".format(i))#pycharts易展示，但不好交互
    return tl

def process_chain(chain):
    line_data = {'x':[],'y':[]}
    poses=[]#[[(lo,loa),(lo,la)],[...]]
    words=[]#[[("words1",fq1),("words2",fq2),("words3",fq3)],[...]]
    frame_ids = []
    table_data = []
    for i in range(len(chain)):
        rows=[]
        e = chain[i]
        pos = []
        word = []
        line_data['y'].append(e["community_docs"])
        line_data['x'].append(str(e["community_frameid"]+1))
        frame_ids.append(e["community_frameid"]+1)
        lats = e["community_lats"]
        lons = e["community_lons"]
        keywords = e["community_keywords"]#array["","",""]
        rigions = e["community_regions"]
        dates = e["community_dates"]
        contents = e["community_contents"]
        cons = e['community_contents']
        for j in range(len(dates)):
            rows.append([str(j+1),dates[j],contents[j],rigions[j],round(lats[j],4),round(lons[j],4)])
        table_data.append(rows)
        for keyword in keywords:
            for w in keyword.split(" "):
                word.append(w)
        words.append(collections.Counter(word).items())
        for k in range(len(lats)):
            la = lats[k]
            lo = lons[k]
            con = cons[k]
            pos.append((lo,la,con))
        poses.append(pos)
    return line_data,poses,words,frame_ids,table_data
            

def event_temp(request):
    print("query event")
    print(chainIdx)
    chain_keys = list(chains.keys())
    chain= chains[chain_keys[int(chainIdx)]]#[{event1},{event2},{event3}]
    context = {}
    timelineIndex = 0
    if 'timelineIndex' in request.GET and request.GET['timelineIndex']:#获得tl的index
        context["timelineIndex"] = request.GET['timelineIndex']
        timelineIndex = int(context["timelineIndex"])
    if 'scrollTop' in request.GET and request.GET['scrollTop']:
        context["scrollTop"] = request.GET['scrollTop']
    line_data,poses,words,frame_ids,table_data = process_chain(chain)
    page = Page()
    print("timelineIdx:{}".format(timelineIndex))
    eventmap = get_eventbmap(poses[timelineIndex])
    eventmap.chart_id = "map_event"
    eventline = get_eventline(line_data)
    eventline.chart_id = "line_event"
    wordcloudline = get_wordcloud_line(words[timelineIndex],frame_ids)
    wordcloudline.chart_id = "wordcloud_line"
    eventtable = get_eventtable(table_data[timelineIndex])
    eventtable.chart_id = "table_event"
    page.add(eventmap)
    page.add(eventline)
    page.add(wordcloudline)
    page.add(eventtable)
    page.render(path="event.html",template_name="simple_page_event.html")
    #记得在以下函数中增加了模板函数
    Page.save_resize_html("event.html", cfg_file="./demo/chart_config_event.json", dest="./demo/templates/my_event_charts.html")
    #page.render("bmap.html",template="simple_page_event.html")
    return render(request,"my_event_charts.html",context)#可以向模板中填充数据来显示矩形框
    #return HttpResponse(page.render_embed(template_name="simple_page_event.html"))

def event(request):
    print("query event")
    print(chainIdx)
    chain_keys = list(chains.keys())
    chain= chains[chain_keys[int(chainIdx)]]#[{event1},{event2},{event3}]
    context = {}
    timelineIndex = 0
    if 'timelineIndex' in request.GET and request.GET['timelineIndex']:#获得tl的index
        context["timelineIndex"] = request.GET['timelineIndex']
        timelineIndex = int(context["timelineIndex"])
    if 'scrollTop' in request.GET and request.GET['scrollTop']:
        context["scrollTop"] = request.GET['scrollTop']
    line_data,poses,words,frame_ids,table_data = process_chain(chain)
    bmap_data = []
    for i in poses[timelineIndex]:
        bmap_data.append({"value":[i[0],i[1],i[2]]})
    for i in range(len(line_data['y'])):
        y_temp = line_data['y'][i]
        x_temp = line_data['x'][i]
        line_data['y'][i]=[x_temp,y_temp]
    print(bmap_data)
    context = {"bmap_data":json.dumps(bmap_data),#用json将其转为字符串，同时模板中加入通道 | safe
               "line_data":line_data
    }
    return render(request,"event.html",context)#可以向模板中填充数据来显示矩形框
    #return HttpResponse(page.render_embed(template_name="simple_page_event.html"))

def get_gridbmap(message) -> BMap:
    BAIDU_AK = "HOTBRAfU1jGcQKHBX15ucKsfZO722eyN"
    pos = (117.20, 39.12)
    #jscode = "console.log('hi hi');"#可嵌入jscode
    #jscode = "functions(param){bmap.addEventListener('click', function(e){alert(e.point.lng + ','+ e.point.lat);});}"
    #每两个点画一条线
    j = [[{"coord":[117.20, 39.12]},{"coord":[118.21, 41.12]}],[{"coord":[119.21, 41.12]},{"coord":[115.21, 41.12]}]]
    c = (
        BMap()
        .add_schema(
            baidu_ak=BAIDU_AK,
            center=[117.20, 39.12],
            zoom = 12
        )
        .add(
            "",
            type_="lines",
            data_pair=j,
            is_polyline=True,
            is_large=False,
            linestyle_opts=opts.LineStyleOpts(color="purple", opacity=0.6, width=1),
        )
        .set_series_opts(effect_opts=opts.EffectOpts(is_show=False),
                        label_opts=opts.LabelOpts(is_show=False))
        .add_control_panel(
            scale_control_opts=opts.BMapScaleControlOpts(),
            navigation_control_opts=opts.BMapNavigationControlOpts(),
            maptype_control_opts=opts.BMapTypeControlOpts(),
            #copyright_control_opts=opts.BMapCopyrightTypeOpts(copyright_="我的")
            #geo_location_control_opts=opts.BMapGeoLocationControlOpts()
            #overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),
        )
        #.add_js_funcs(jscode)
        #.set_global_opts(title_opts=opts.TitleOpts(title="BMap-基本示例"))
    )
    return c

#def preprocess_chains_tempplates(chains,lengend_status,global_event=True):#按模板渲染的方式处理chains
    #chains：事件链
    #lengend_status: 图例状态

def test(request):
    return

def event_chain(request):
    request.encoding='utf-8'
    global frames
    global chains
    global chainIdx
    global date_begin_old
    global date_end_old
    global timeInterval_old
    global bursty_dict
    global colors_table
    lengend_status = None
    is_ajax = False#如果是ajax 要重新计算
    #colors_table = getColor(24)

    if request.method == 'POST' and request.is_ajax():
        received_json_data = json.loads(request.body)#获得是一个dict 可以查看每个图例被选中的状态
        is_ajax = True
        if(received_json_data):
            lengend_status = received_json_data["lengend_status"]

    if(not is_ajax): #如果是ajax 即该变图例状态修渲染部分的话不用重新事件检测 
        #if(date_begin_old==""):
        date_begin = "2015/11/10 00:00:00"
        #if(date_end_old==""):
        date_end = "2015/11/12 00:00:00"
        timeInterval = 24
        #num_frames = 5
        #如果有查询序号就执行查看event页面
        if 'chainIdx' in request.GET and request.GET['chainIdx']:
            chainIdx = int(request.GET['chainIdx'])-1#下标从0开始，所以要减一
            return event(request)
        if 'date_begin' in request.GET and request.GET['date_begin']:
            date_begin = request.GET['date_begin']+" "+"00:00:00"
            date_begin = date_begin.replace("-","/")
            print("databigin:{}".format(date_begin))
        if 'date_end' in request.GET and request.GET['date_end']:
            date_end = request.GET['date_end']+" "+"00:00:00"
            date_end = date_end.replace("-","/")
            print("dataend:{}".format(date_end))

        num_frames = int((time2timestamp(date_end)-time2timestamp(date_begin))/(3600*timeInterval))
        print("num_frames:{}".format(num_frames))
        #如果获得经度和维度,就可以在process.detect中删除不在这经度和维度范围内的数据 to do
        if(date_begin_old!=date_begin or date_end_old !=date_end or timeInterval_old!=timeInterval):#如果有一个更新
            frames = process.detect(date_begin,3600*timeInterval,num_frames)
            chains = process.match(frames)
            chains,bursty_dict = preprocess_chains(chains)#对chains做一些处理按bursty、glbal/local处理
            colors_table = getColor(len(chains))#每条事件链都用不同的颜色标注
            #不论是全城还是局部事件都要对chain做预处理操作，并且只返回前top20的事件链
        date_begin_old = date_begin
        date_end_old = date_end
        timeInterval_old = timeInterval

    line_data,themeriver_data,themeriver_lengend, pos,words = process_data(frames,chains,bursty_dict,colors_table,lengend_status)
    wordcloud_data = []
    bmap_data = []
    for i in range(len(line_data['y'])):
        y_temp = line_data['y'][i]
        x_temp = line_data['x'][i]
        line_data['y'][i]=[x_temp,y_temp]
    for i in words:
        wordcloud_data.append({"name":i[0],"value":i[1]})
    for i in pos:
        bmap_data.append({"name":i[0],"value":[i[2],i[1],i[4]],"itemStyle":{"color":i[3]}})

    context = {"bmap_data":json.dumps(bmap_data),#用json将其转为字符串，同时模板中加入通道 | safe
               "wordcloud_data":json.dumps(wordcloud_data),
               "themeriver_data":json.dumps(themeriver_data),
               "line_data":line_data,#好像对于字典这样的数据不用json.dumps啊
               "themeriver_color":json.dumps(colors_table),
               "mytitle":"天津城市突发性事件预警系统——NEW"}
    if request.is_ajax():
        data = {
            "wordcloud_data":wordcloud_data,
            "bmap_data":bmap_data,
            "line_data":line_data,
            "status":"success"}
        response = JsonResponse(data)
        return response
    return render(request,"test.html",context)
'''
words = [
    ("Sam S Club", 10000),
    ("Macys", 6181),
    ("Amy Schumer", 4386),
    ("Jurassic World", 4055),
    ("Charter Communications", 2467),
    ("Chick Fil A", 2244),
    ("Planet Fitness", 1868),
    ("Pitch Perfect", 1484),
    ("Express", 1112),
    ("Home", 865),
    ("Johnny Depp", 847),
    ("Lena Dunham", 582),
    ("Lewis Hamilton", 555),
    ("KXAN", 550),
    ("Mary Ellen Mark", 462),
    ("Farrah Abraham", 366),
    ("Rita Ora", 360),
    ("Serena Williams", 282),
    ("NCAA baseball tournament", 273),
    ("Point Break", 265),
    ]

'''