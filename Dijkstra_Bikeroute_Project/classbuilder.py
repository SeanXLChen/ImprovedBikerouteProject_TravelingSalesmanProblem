import math
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import LineString, Point
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

R = 6371  # Earth radius in km

class Vectex:
    """
    A node class representing a vertex in a linked list.
    """
    def __init__(self, datapoint, info):
        self.datapoint = datapoint
        self.info = info
        self.next = None
        # self.prev = None

class AdjacentLinkedList:
    """
    A class representing a linked list for use in the Graph class.

    Will contain all the adjecent vertices to one vertex
    """

    def __init__(self):
        self.head = None

    def append(self, datapoint, info):
        """
        Appends a new node with the given datapoint and info to the end of the list.
        
        :param datapoint: The datapoint to be stored in the new node.
        :param info: Additional information to be stored in the new node.
        """
        new_node = Vectex(datapoint, info)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

class Graph:
    """
    A class representing a graph for modeling the bikeways, parks, and schools in a city.
    """
    def __init__(self):
        self.vertices = {}
    
    def add_vertex(self, coordinate):
        """
        Adds a vertex to the graph with the given coordinate.

        :param coordinate: A tuple containing the latitude and longitude of the vertex.
        """
        if coordinate not in self.vertices:
            self.vertices[coordinate] = AdjacentLinkedList()
        
        # current_node = self.vertices[coordinate].head
        # while current_node is not None:
        #     print(current_node.datapoint, end=" <-> ")
        #     current_node = current_node.next
        # print("None")
    
    def add_edge(self, coord1, coord2, info1, info2, distance):
        """
        Adds an edge between two vertices with the given coordinates and information.

        :param coord1: A tuple containing the latitude and longitude of the first vertex.
        :param coord2: A tuple containing the latitude and longitude of the second vertex.
        :param info1: Additional information about the first vertex.
        :param info2: Additional information about the second vertex.
        :param distance: The distance between the two vertices.
        """
        if coord1 in self.vertices and coord2 in self.vertices:
            self.vertices[coord1].append((coord2, distance), info2)
            self.vertices[coord2].append((coord1, distance), info1)
        else:
            raise ValueError("Both coordinates must be in the graph before creating an edge.")

    def haversine_distance(self, coord1, coord2):
        """
        Calculates the haversine distance between two coordinates.

        :param coord1: A tuple containing the latitude and longitude of the first coordinate.
        :param coord2: A tuple containing the latitude and longitude of the second coordinate.
        :return: The haversine distance between the two coordinates in kilometers.
        """
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def build_graph(self, parsed_datapoint, geom_index):
        """
        Builds the graph using parsed datapoint and a specified geometry index.

        :param parsed_datapoint: A list of lists containing the parsed datapoint.
        :param geom_index: An integer representing the index of the geometry column in the datapoint.
        """
        for row in parsed_datapoint[1:]:
            coordinates = row[geom_index]
            info1 = row[:geom_index] + row[geom_index + 1:]
            info2 = row[:geom_index] + row[geom_index + 1:]
            for i in range(len(coordinates) - 1):
                coord1 = tuple(coordinates[i])
                coord2 = tuple(coordinates[i + 1])
                self.add_vertex(coord1)
                self.add_vertex(coord2)
                distance = self.haversine_distance(coord1, coord2)
                self.add_edge(coord1, coord2, info1, info2, distance)    
    
    def find_closest_vertex(self, coordinate):
        """
        Finds the closest vertex to the given coordinate.

        :param coordinate: A tuple containing the latitude and longitude of the coordinate.
        :return: A tuple containing the closest vertex and its distance from the given coordinate.
        """
        min_distance = float('inf')
        closest_vertex = None

        for vertex in self.vertices:
            distance = self.haversine_distance(coordinate, vertex)
            if distance < min_distance:
                min_distance = distance
                closest_vertex = vertex

        return closest_vertex, min_distance

    def add_park_coordinates(self, park):
        """
        Adds park coordinates to the graph.

        :param park: A Park instance containing park information and coordinates.
        """
        for coordinate in park.coordinates:
            closest_vertex, min_distance = self.find_closest_vertex(coordinate)
            self.add_vertex(tuple(coordinate))
            self.add_edge(tuple(coordinate), closest_vertex, park.name, park.name, min_distance)

    def get_neighbors(self, vertex):
        """
        Returns the neighbors of the given vertex.

        :param vertex: A tuple containing the latitude and longitude of the vertex.
        :return: A list of tuples containing neighbor vertices, their info, and edge distances.
        """
        if vertex not in self.vertices:
            raise ValueError("The specified vertex does not exist in the graph.")
        neighbors = []
        adjacency_list = self.vertices[vertex]
        current = adjacency_list.head
        while current:
            neighbor, edge_distance = current.datapoint
            info = current.info
            neighbors.append((neighbor, info, edge_distance))
            current = current.next
        return neighbors

    def find_shortest_path(self, graph_instance, school_instance, selected_park):
        """
        Finds the shortest path between a school and a park using Dijkstra's algorithm.

        :param graph_instance: A Graph instance representing the bikeways network.
        :param school_instance: A School instance containing school information and coordinates.
        :param selected_park: A Park instance containing park information and coordinates.
        :return: A list of vertices representing the shortest path between the school and the park.
        """    
        # Add park coordinates to the graph
        graph_instance.add_park_coordinates(selected_park)

        # Add school coordinates to the graph
        graph_instance.add_park_coordinates(school_instance)

        # Initialize datapoint structures for Dijkstra's algorithm
        unvisited_vertices = set(graph_instance.vertices)
        distances = {vertex: float('inf') for vertex in graph_instance.vertices}
        distances[tuple(school_instance.coordinates[0])] = 0
        previous_vertices = {vertex: None for vertex in graph_instance.vertices}

        while unvisited_vertices:
            current_vertex = min(
                unvisited_vertices, key=lambda vertex: distances[vertex])
            unvisited_vertices.remove(current_vertex)

            for neighbor, info, edge_distance in graph_instance.get_neighbors(current_vertex):
                distance = distances[current_vertex] + edge_distance

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex

        # Reconstruct the shortest path to the park
        shortest_path = []
        min_distance = float('inf')
        park_vertex = None

        # Check for the shortest distance to any park coordinate
        for park_coord in selected_park.coordinates:
            park_tuple = tuple(park_coord)
            if distances[park_tuple] < min_distance:
                min_distance = distances[park_tuple]
                park_vertex = park_tuple

        if park_vertex is None:
            raise ValueError("No path found") # No path found

        current_vertex = park_vertex
        while current_vertex is not None:
            shortest_path.append(current_vertex)
            current_vertex = previous_vertices[current_vertex]

        return shortest_path[::-1]
    

    def plot_graph(self, shortest_path=None):

        """
        Plots the graph using GeoPandas and matplotlib. The graph vertices are shown as blue points,
        and the edges are shown as red lines. If a shortest path is provided, it will be plotted
        as a green line.

        Args:
            shortest_path (list, optional): A list of tuples containing the latitude and longitude
                                            coordinates of the shortest path. Defaults to None.

        Raises:
            ValueError: If the graph is empty.
        """
        if not self.vertices:
            raise ValueError("The graph is empty. Add vertices before plotting.")

        # Prepare the data for GeoPandas
        edge_list = []
        point_list = []
        for vertex, adjacency_list in self.vertices.items():
            lat1, lon1 = vertex
            point_list.append(Point(lat1, lon1))
            current = adjacency_list.head
            while current:
                coord2, _ = current.datapoint
                lat2, lon2 = coord2
                edge_list.append(LineString([(lat1, lon1), (lat2, lon2)]))
                current = current.next

        # Create GeoDataFrames for the edges and vertices
        edges_gdf = gpd.GeoDataFrame(geometry=edge_list)
        vertices_gdf = gpd.GeoDataFrame(geometry=point_list)

        # Plot the graph
        fig, ax = plt.subplots(figsize=(10, 10))
        edges_gdf.plot(ax=ax, linewidth=2, edgecolor='red')
        vertices_gdf.plot(ax=ax, markersize=1, color='blue', marker='o')

        # Plot the shortest path if provided
        if shortest_path:
            path_coords = [(lat,lon) for lat, lon in shortest_path]
            path_line = LineString(path_coords)
            path_gdf = gpd.GeoDataFrame(geometry=[path_line])
            path_gdf.plot(ax=ax, linewidth=3, edgecolor='green')

        # Configure plot settings
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Bikeways Graph')
        ax.grid(True)

        plt.show()

