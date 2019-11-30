from django.shortcuts import render

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
def get_themeriver():
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
    themeriver = (
        ThemeRiver()
        .add(
            ["DQ", "TY", "SS", "QG", "SY", "DD"],
            data,
            singleaxis_opts=opts.SingleAxisOpts(type_="time", pos_bottom="70%"),#可以通过调整坐标轴来调整图的位置
            label_opts = opts.LabelOpts(is_show=False)
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="事件链"),
                        legend_opts=opts.LegendOpts(type_ = 'scroll',pos_left="4%",pos_bottom='40%',orient='vertical'))
                        #datazoom_opts=opts.DataZoomOpts())#图例设置
                        
    )
    return themeriver

def get_line():
    line = (
        Line()
        .add_xaxis(Faker.choose())
        #.add_yaxis("商家A", Faker.values())
        
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="天津政府服务热线数目变化", pos_right="center"),
            legend_opts=opts.LegendOpts(is_show=False),
            #legend_opts=opts.LegendOpts(pos_top="20%"),
            datazoom_opts=opts.DataZoomOpts(),
            #toolbox_opts=opts.ToolboxOpts(orient='vertical',pos_right="right")
        )
    )
    
    return line



def get_bmap(message) -> BMap:
    BAIDU_AK = "HOTBRAfU1jGcQKHBX15ucKsfZO722eyN"
    pos = (117.20, 39.12)
    c = (
        BMap()
        .add_schema(
            baidu_ak=BAIDU_AK,
            center=[117.20, 39.12],
            zoom = 10,
            is_roam=False
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

def get_mymap(message) -> Geo:
    pos = (117.20, 39.12)
    tianjing_map = (
         Geo()
        .add_schema(maptype="北京",is_roam=False)
        # 加入自定义的点，格式为
        .add_coordinate("测试点", pos[0],pos[1])
        #.add_coordinate_json("./demo/coord.json")
        # 为自定义的点添加属性
        .add("测试点",[("测试点", 51)],type_="effectScatter")
        #.set_series_opts()
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                         effect_opts=opts.EffectOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title=message,pos_right="center"),
                        )
    )
    return tianjing_map

def event_chain(request):
    '''
    grid = (
        Grid()
        .add(get_line(), grid_opts=opts.GridOpts(pos_left="55%"))
        .add(get_mymap(), grid_opts=opts.GridOpts(pos_right="50%"))
    )
    '''
    request.encoding='utf-8'
    if 'date_begin' in request.GET and request.GET['date_begin']:
        message = '你搜索的内容为: ' + request.GET['date_begin']
    else:
        message = '天津市地图'

    page = Page(layout=Page.DraggablePageLayout)
    mymap = get_bmap(message)
    #mymap = get_mymap(message)
    mymap.chart_id = "bmap_1"
    myline = get_line()
    myline.chart_id = "line_1"
    mythemeriver = get_themeriver()
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
        tl.add(wordcloud, "{}年".format(i))
    return tl

def event(request):
    page = Page(layout=Page.DraggablePageLayout)
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
    Page.save_resize_html("event.html", cfg_file="./demo/chart_config_event.json", dest="./demo/templates/my_event_charts.html")
    #page.render("bmap.html",template="simple_page_event.html")
    return render(request,"my_event_charts.html")#可以向模板中填充数据来显示矩形框
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
    
    eventmap.render("bmap.html")
    #print(eventmap.bmap_js_functions)
    return HttpResponse(eventmap.render_embed())