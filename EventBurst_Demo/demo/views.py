from django.shortcuts import render
import numpy as np
import collections
# Create your views here.
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig, SymbolType
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./demo/templates"))

from pyecharts import options as opts
from pyecharts.charts import Page, ThemeRiver, Bar, Map, Geo, Grid, Line, Scatter, Timeline,WordCloud, BMap
from pyecharts.faker import Collector, Faker

from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import os
import sys
#sys.path.append("..")
from mycommunity.process import Process
#print(sys.path)
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
def get_themeriver(data,lengend):
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
            singleaxis_opts=opts.SingleAxisOpts( pos_bottom="50%",min_=1),#可以通过调整坐标轴来调整图的位置
            label_opts = opts.LabelOpts(is_show=False)
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="事件链"),
                         tooltip_opts=opts.TooltipOpts(is_show=True,trigger_on="mousemove|click"),
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
            )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="帧数",splitarea_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(
                name="举报数目",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True,
            ),
            #title_opts=opts.TitleOpts(title="天津政府服务热线数目变化", pos_right="center"),
            legend_opts=opts.LegendOpts(is_show=False),
            #legend_opts=opts.LegendOpts(pos_top="20%"),
            datazoom_opts=opts.DataZoomOpts(range_start=0,range_end=100),
            #xaxis_opts=opts.AxisOpts(type_="value")#经轴是数值value
            #toolbox_opts=opts.ToolboxOpts(orient='vertical',pos_right="right")
        )
    )
    
    return line


def get_bmap(pos) -> BMap:
    BAIDU_AK = "HOTBRAfU1jGcQKHBX15ucKsfZO722eyN"
    center = (117.20, 39.12)
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
        sequence.append((str(i),0.1))
    c.add(
        "投诉坐标",#系列名称
        sequence,
        type_="scatter",#"heatmap" 可以切换显示的类型热力图或散点图
        label_opts=opts.LabelOpts(formatter="{b}"),
    )
    #.add("bmap",
        #[{"coord":[117.21, 39.13],"sim":10},{"coord":[117.20, 39.13],"sim":20},{"coord":[117.21, 39.12],"sim":5}],
        #[list(z) for z in zip(Faker.provinces, Faker.values())],#zip将迭代对像打包成元组最后的结果是[['浙江',v1],['广东',v2]]
        #[[117.21, 39.13],[117.20, 39.12],[117.22, 39.10],[117.25, 39.11],[117.19, 39.02],[117.20, 39.12]],
        #type_="heatmap",
        #label_opts=opts.LabelOpts(formatter="{b}"))
    c.set_series_opts(effect_opts=opts.EffectOpts(is_show=True),
                    label_opts=opts.LabelOpts(is_show=False))
    c.add_control_panel(
        scale_control_opts=opts.BMapScaleControlOpts(),
        navigation_control_opts=opts.BMapNavigationControlOpts(),
        maptype_control_opts=opts.BMapTypeControlOpts())
        #copyright_control_opts=opts.BMapCopyrightTypeOpts(copyright_="我的")
        #geo_location_control_opts=opts.BMapGeoLocationControlOpts()
        #overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),
    c.set_global_opts(visualmap_opts=opts.VisualMapOpts())
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

def process_data(frames,chains):
    #frames[[{event1},{event2}],[{event1},{event2}]]
    #chain{"key":[{event1}->{event2}->{event2}]}
    line_data = {'x':[],'y':[]}#画折线图只要x轴和y轴的数据
    themeriver_data =[]       #[["第i帧数",事件链在第i帧举报数目,"事件链关键词"]]
    themreiver_lengend = []
    pos = []#每条举报数据的位置
    idx = 1
    pos_idx = 0
    for i in range(len(frames)):
        frame = frames[i]
        line_data['x'].append(str(i+1))#帧的序号,x轴是str类型
        y = 0
        for e in frame:
            y+=len(e)
        line_data['y'].append(y)#每帧的举报数目
    #print(chains)
    for k,v in chains.items():
        chain = v#[{},{},{}] ...
        abstract = " "+str(idx)+" "  #每条事件链的摘要
        idx+=1
        temp = []
        for e in chain:#事件链上的每个结点
            keywords = e["community_keywords"]#array["","",""]
            lats = e["community_lats"]
            lons = e["community_lons"]
            for k in keywords:
                for w in k.split(" "):
                    temp.append(w)
            for i in range(len(lats)):
                la = lats[i]
                lo = lons[i]
                pos.append((str(pos_idx),la,lo))
                pos_idx += 1
        C = np.array(collections.Counter(temp).most_common())#[("word":num)]
        if(len(C)<20):
            e = len(C)
        else:
            e = 20
        for i in range(e):
            abstract+=C[i][0]
            abstract+=" "#事件链的摘要
        themreiver_lengend.append(abstract)
        for e in chain:
            frame_id = str(e["community_frameid"]+1)
            num_docs = e["community_docs"]
            themeriver_data.append([frame_id,num_docs,abstract])
    #print(themreiver_lengend)
    return line_data,themeriver_data,themreiver_lengend,pos

def event_chain(request):
    '''
    grid = (
        Grid()
        .add(get_line(), grid_opts=opts.GridOpts(pos_left="55%"))
        .add(get_mymap(), grid_opts=opts.GridOpts(pos_right="50%"))
    )
    '''
    request.encoding='utf-8'
    #如果有查询序号就执行查看event页页
    if 'chainIdx' in request.GET and request.GET['chainIdx']:
        print("bigin to url: chain")
        return event(request)
    if 'date_begin' in request.GET and request.GET['date_begin']:
        message = '你搜索的内容为: ' + request.GET['date_begin']
    else:
        message = '天津市地图'
    frames = process.detect("2015/11/05 00:00:00",3600*24,2)
    #line_data = frames
    chains = process.match(frames)
    #print(chain)
    line_data,themeriver_data,themeriver_lengend, pos = process_data(frames,chains)
    page = Page()
    mymap = get_bmap(pos)
    #mymap = get_mymap(message)
    mymap.chart_id = "bmap_1"
    myline = get_line(line_data)
    myline.chart_id = "line_1"
    mythemeriver = get_themeriver(themeriver_data,themeriver_lengend)
    mythemeriver.chart_id = "themeriver_1"
    # 需要自行调整每个 chart 的 height/width，显示效果在不同的显示器上可能不同
    page.add(mymap)
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

def get_eventline():
    line = (
        Line()
        .add_xaxis(Faker.choose())
        #.add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="天津政府服务热线数目", pos_right="center"),
            legend_opts=opts.LegendOpts(is_show=False),
            #legend_opts=opts.LegendOpts(pos_top="20%"),
            datazoom_opts=opts.DataZoomOpts(),
            #toolbox_opts=opts.ToolboxOpts(orient='vertical',pos_right="right")
        )
    )
    
    return line
def get_eventtable() -> Table:
    table = Table()

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
    table.add(headers, rows).set_global_opts(
        title_opts=ComponentTitleOpts(title="详细举报数据"),
    )
    return table

def get_wordcloud_line()->Line:
    tl = Timeline()
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
    for i in range(2015, 2020):
        wordcloud = (
            WordCloud()
            .add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="事件链词云图"))
            
        )
        tl.add(wordcloud, "{}年".format(i))#pycharts易展示，但不好交互
        #tl.add()
        #tl.
        #tl.add(Bar(),"{}年".format(i))
    #print()
    #tl.__getattribute__("timepoint")
    return tl

def event(request):
    print(request)
    print("query event")
    context = {}
    if 'timelineIndex' in request.GET and request.GET['timelineIndex']:#获得tl的index
        context["timelineIndex"] = request.GET['timelineIndex']
    if 'scrollTop' in request.GET and request.GET['scrollTop']:
        context["scrollTop"] = request.GET['scrollTop']
    page = Page()
    eventmap = get_eventbmap(message="天津市地图")
    eventmap.chart_id = "map_event"
    eventline = get_eventline()
    eventline.chart_id = "line_event"
    wordcloudline = get_wordcloud_line()
    wordcloudline.chart_id = "wordcloud_line"
    eventtable = get_eventtable()
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

def test(request):
    #scatter = get_scatter()
    eventmap = get_gridbmap(message="天津市地图")
    eventmap.chart_id = 'bmap_test'
    page = Page()
    page.add(eventmap)
    #eventmap.render("bmap.html")
    #print(eventmap.bmap_js_functions)
    return HttpResponse(page.render_embed())