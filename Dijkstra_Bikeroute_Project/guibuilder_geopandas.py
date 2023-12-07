import tkinter as tk
import geopandas 
import folium # with geopandas
import webbrowser
import os

VANCOUVER_CENTER = (49.2827, -123.1207)

class App:
    """A class to represent the GUI application to find and visualize the shortest path."""

    def __init__(self, root, graph, parks, startpoint, boundary_data_gpd):
        """Initializes the App class.

        Parameters:
        -----------
        root : tkinter.Tk
            The main application window.
        graph : Graph
            The graph representation of the road network.
        parks : List[Park]
            The list of parks in the area.
        startpoint : Tuple[float, float]
            The coordinates of the startpoint.
        boundary_data_gpd : geopandas.GeoDataFrame
            The boundary data of the area.
        """
        self.root = root
        self.graph = graph
        self.parks = parks
        self.startpoint = startpoint
        self.boundary_data_gpd = boundary_data_gpd.dropna(subset=['geometry'])

        self.root.title("Find a Park")

        self.boundary_coords = [list(polygon.exterior.coords) for polygon in boundary_data_gpd.geometry]

       # make a frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand = True)

        # Dropdown menu with park names
        self.park_var = tk.StringVar(self.main_frame)
        self.park_var.set("Select a park")
        self.park_dropdown = tk.OptionMenu(self.main_frame, self.park_var, *[park.name for park in self.parks])
        self.park_dropdown.pack()

        # User enter the coordinates to init the startpoint class: defalut is school location
        self.instruction = tk.Label(self.main_frame, text="Please Enter the Coordinates as startpoint, by default is NEU Cooridinates")
        self.instruction.pack()

        self.lat_lable = tk.Label(self.main_frame, text="Latitude:")
        self.lat_lable.pack()
        self.lat_entry = tk.Entry(self.main_frame)
        self.lat_entry.pack()

        self.lon_label = tk.Label(self.main_frame, text="Longitude:")
        self.lon_label.pack()
        self.lon_entry = tk.Entry(self.main_frame)
        self.lon_entry.pack()

        # Button to confirm the cooridinates that user just entered
        self.submit_button = tk.Button(self.main_frame, text="Confirm Cooridinates", command=self.submit_coordinates)
        self.submit_button.pack()


        # Button to draw the path to the selected park
        self.draw_button = tk.Button(self.main_frame, text="Show path", command=self.draw_path_to_park)
        self.draw_button.pack()

        # Canvas to display the graph
        self.canvas = tk.Canvas(self.main_frame, width=600, height=300)
        self.canvas.pack()


    def draw_path_to_park(self):
        """Gets the selected park from the dropdown, calculates the shortest path to it,
        generates a folium map with the path and opens it in the default browser."""
        ... 
        try:
            # Get the selected park
            selected_park_name = self.park_var.get()
            selected_park = next((park for park in self.parks if park.name == selected_park_name), None)

            if selected_park:
                # Calculate the shortest path to the selected park
                path = self.graph.find_shortest_path(self.graph, self.startpoint, selected_park)


                if path:
                    # Draw the path on the map
                    folium_map = self.create_folium_map(self.boundary_coords, path)

                    # Save the map as an HTML file
                    map_file = os.path.join(os.getcwd(), "map.html")
                    folium_map.save(map_file)

                    # Open the generated HTML file in the default browser
                    if webbrowser.open(map_file):
                    
                        # Draw the path on the graph
                        img = self.graph.plot_graph(path)
                        # Update the canvas with the new image
                        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
                else:
                    print("No path found to the selected park.")
            else:
                print("No park selected.")
        except Exception as e:
            print(f"An error occurred while drawing the path to the park: {e}")


    def create_initial_map(self, map_center=VANCOUVER_CENTER, zoom_start=10):
        m = folium.Map(location=map_center, tiles="OpenStreetMap", zoom_start=zoom_start)
        self.display_map_in_tkinter(self.map_frame, m)

    def create_folium_map(self, boundary_coords, shortest_path, map_center=VANCOUVER_CENTER, zoom_start=10):
        """Creates a folium map and adds the boundary, graph, and shortest path to it.

        Parameters:
        -----------
        boundary_coords : List[List[Tuple[float, float]]]
            The coordinates of the boundary.
        shortest_path : List[Tuple[float, float]]
            The coordinates of the shortest path.
        map_center : Tuple[float, float], optional
            The center coordinates of the map, by default VANCOUVER_CENTER.
        zoom_start : int, optional
            The zoom level of the map, by default 10.

        Returns:
        --------
        folium.folium.Map
            The generated folium map.
        """
        m = folium.Map(location=map_center, tiles="OpenStreetMap",zoom_start=zoom_start)        

        # for coords in self.boundary_coords:
        if boundary_coords:
            for each_boundary_coords in boundary_coords:
                folium.Polygon(locations=each_boundary_coords, color="blue", weight=3, fill_color="blue", fill_opacity=0.1).add_to(m)


        # Draw the bikeway path
        if self.graph:
            for vertex, adjacency_list in self.graph.vertices.items():
                lat1, lon1 = vertex
                folium.CircleMarker([lon1, lat1], radius=0.3, color='blue', fill=True, fill_color='blue', fill_opacity=1).add_to(m)
            
                current = adjacency_list.head
                while current:
                    coord2, info = current.datapoint
                    lat2, lon2 = coord2
                    folium.CircleMarker(coord2, radius=0.3, color='blue', fill=True, fill_color='blue', fill_opacity=1).add_to(m)
                    path_coord = [[lon2, lat2], [lon1, lat1]]
                    folium.PolyLine(path_coord, color = 'red', weight = 1).add_to(m)
                    current = current.next

        # Draw the shortest path
        if shortest_path:
            shortest_path_lonlat_form = []
            for i in shortest_path:
                lat, lon = i
                lonlat_form_path = [lon, lat]
                shortest_path_lonlat_form.append(lonlat_form_path)
            folium.PolyLine(shortest_path_lonlat_form, color = 'green', weight = 6).add_to(m)
        
        return m
    
    def submit_coordinates(self):
        """
        Retrieves the user's input for latitude and longitude from the Entry widgets.
        If the user has provided valid input, updates the startpoint's coordinates.
        If no input is provided, the startpoint's coordinates remain unchanged.
        """
        self.lat_input = self.lat_entry.get()
        self.lon_input = self.lon_entry.get()

        if len(self.lat_input) != 0 and len(self.lon_input) != 0:
            lat = float(self.lat_input)
            lon = float(self.lon_input)
            self.startpoint.coordinates = [(lat, lon)]

