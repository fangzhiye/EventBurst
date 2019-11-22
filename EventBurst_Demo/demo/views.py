from django.shortcuts import render

# Create your views here.
from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from django.http import HttpResponse

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./demo/templates"))

from pyecharts import options as opts
from pyecharts.charts import Page, ThemeRiver, Bar, Map, Geo, Grid, Line, Scatter
from pyecharts.faker import Collector, Faker

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
            singleaxis_opts=opts.SingleAxisOpts(type_="time", pos_bottom="10%"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="ThemeRiver-基本示例"))
    )
    return themeriver

def get_line():
    line = (
        Line()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Grid-Line", pos_right="5%"),
            legend_opts=opts.LegendOpts(pos_right="20%"),
        )
    )
    
    return line

def get_scatter() -> Scatter:
    scatter = (
        Scatter()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Grid-Scatter"),
            legend_opts=opts.LegendOpts(pos_left="20%"),
        )
    )
    return scatter

def get_mymap(message) -> Geo:
    tianjing_map = (
         Geo()
        .add_schema(maptype="天津")
        # 加入自定义的点，格式为
        .add_coordinate("测试点", 117.20, 39.12)
        # 为自定义的点添加属性
        .add("geo", [("测试点", 51)])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title=message))
    )
    return tianjing_map

def test(request):
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
        message = '你提交了空表单'

    page = Page(layout=Page.DraggablePageLayout)
    mymap = get_mymap(message)
    mymap.chart_id = "map_1"
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