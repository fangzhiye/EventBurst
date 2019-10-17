import networkx as nx
import matplotlib.pyplot as plt
import pyecharts
from pyecharts.charts.basic_charts.graph import Graph

G = nx.Graph()
nodes = [(1,{'color':'red'}),(2,{'color':'blue'}),(3,{'color':'black'}),(4,{'color':'white'})]#增加结点和结点属性
edges = [(1,2,{'weight':2}),(1,3,{'weight':2}),(3,2,{'weight':2}),(4,2,{'weight':2}),(1,4,{'weight':2})]
G.add_edges_from(edges)
G.add_nodes_from(nodes)
#print(list(G.nodes()))

r_nodes = [{"name":"","value":0,"symbolSize":10} for i in range(G.number_of_nodes())]
for i,name in enumerate(G.nodes()):
	print(i,name)
	r_nodes[i]["name"] = name
	r_nodes[i]["value"] = G.degree()[name]
	r_nodes[i]["symbolSize"] = G.degree()[name]
r_links = [{"source":"","targe":""} for i in range(G.number_of_edges())]
for i,(u,v) in enumerate(G.edges()):
	r_links[i]["source"] = u
	r_links[i]["target"] = v
	r_links[i]["value"] = G[u][v]["weight"]
graph = Graph()
graph.add("",r_nodes,r_links)
graph.render("./test.html")
graph
