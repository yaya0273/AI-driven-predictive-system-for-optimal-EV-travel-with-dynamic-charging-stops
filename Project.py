import json
from copy import deepcopy
import csv

def load_json(filename): #Loads a graph data structure from a JSON file.
  with open(filename, 'r') as f:
    graph_json = json.load(f)
  graph = {}
  for entry in graph_json:
    city = entry["city"]
    neighbors = entry["neighbors"]
    graph[city] = neighbors
  return graph

def find_shortest_path(graph, start, goal, max_distance):  #Finds the shortest path between two nodes in a graph, considering edge distance threshold. Saves the path into a CSV file.
  shortest_distance = {} 
  track_predecessor = {} 
  unseenNodes = deepcopy(graph) 
  infinity = 9999 
  track_path = [] 
  for node in unseenNodes:
      shortest_distance[node] = infinity
  shortest_distance[start] = 0
  while unseenNodes:
      min_distance_node = None
      for node in unseenNodes:
          if min_distance_node is None:
              min_distance_node = node
          elif shortest_distance[node] < shortest_distance[min_distance_node]:
              min_distance_node = node
      path_options = graph[min_distance_node].items()
      for child_node, weight in path_options:
              if weight + shortest_distance[min_distance_node] < shortest_distance[child_node] and weight<max_distance:
                  shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
                  track_predecessor[child_node] = min_distance_node
      unseenNodes.pop(min_distance_node)
  currentNode = goal
  while currentNode != start:
      try:
          track_path.insert(0,currentNode)
          currentNode = track_predecessor[currentNode]
      except KeyError:
          print('Path not reachable')
          return
  track_path.insert(0,start)
  return track_path
  
def create_csv(track_path,max_distance):
    with open("Travel Plan.csv",'w',newline='') as f:
        csvr=csv.writer(f)
        csvr.writerow(['From','To','Distance(km)','Charge Required(%)'])
        for i in range(len(track_path)-1):
            d=round(graph[track_path[i]][track_path[i+1]])
            csvr.writerow([track_path[i],track_path[i+1],d,round(d/max_distance*100)])


graph = load_json("dataset.json")
source="Pune"
dest="Kochi"
car_range=200
path=find_shortest_path(graph,source,dest,car_range)
create_csv(path,car_range)

