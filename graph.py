import json
from networkx.readwrite import json_graph

"""
    @procedure get_graph() Returns graph of the city's sectors.
"""
def get_graph():

    with open("sectorGraph/sectorGraphProcessed.json") as data_file:
       data = json.load(data_file)

    sectorGraph = json_graph.adjacency_graph(data)
    return sectorGraph

"""
    @procedure get_TravelTime() Returns travel time between nodes in minutes.
"""
def get_TravelTime(graph,origin,destination):
    time = graph[origin][destination]['travelTime']
    return time // 60 #Converts time from seconds to minutes
