import requests
import json
from bs4 import BeautifulSoup
import googlemaps
gmaps = googlemaps.Client(key="AIzaSyCJgK_1nPD78QvQ9Cf6ICFojTEZnsV-7LI")

def calc_dist(org,dest):    #Calculates distance from the origin to the destination 
                            #using google maps distance matrix API.
  try:
    distance_matrix = gmaps.distance_matrix(org, dest)
    distance = distance_matrix["rows"][0]["elements"][0]["distance"]["value"]/1000
    return distance
  except:
    return float('inf')

def get_cities():  #Gets the list of all the cities present in the wikipedia page url, 
                  #ie all cities with greater than 100,000 population.
  url = "https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  tables = soup.find_all('table', class_='wikitable')
  cities = []
  for table in tables:
    for row in table.find_all('tr')[1:]:  
        try:
            city_name = int(row.find_all('td')[0].text.strip())  
            city_name=row.find_all('td')[1].text
        except:
           city_name=row.find_all('td')[0].text
        city_name=''.join([i for i in city_name if i.isalpha()])
        cities.append(city_name)
  return cities

def create_graph(major_cities):  #Creates a graph data structure where 
                                #each node represents a city and the 
                                #edges represnt the distance between the nodes.
  graph = {}
  for city in major_cities:
    graph[city] = {}
    for other_city in major_cities:
      if city != other_city:  # Avoid self-loops
        dist = calc_dist(city, other_city)
        print(city,other_city,dist)
        graph[city][other_city] = dist
  return graph

def save_graph_json(graph):  #Saves the graph in JSON format.
  graph_json = []
  for city, neighbors in graph.items():
    neighbor_distances = {neighbor: distance for neighbor, distance in neighbors.items()}
    graph_json.append({"city": city, "neighbors": neighbor_distances})

  with open('Dataset.json', 'w') as f:
    json.dump(graph_json, f, indent=2)  


major_cities = get_cities()  
graph=create_graph(major_cities)  
save_graph_json(graph)

