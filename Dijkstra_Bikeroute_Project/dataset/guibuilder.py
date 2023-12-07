import tkinter as tk
from PIL import ImageTk

class App:
    """A class to represent the GUI application to find and visualize the shortest path to a park."""

    def __init__(self, root, graph, parks, school):
        """
        Initialize the application.

        Args:
            root (Tk): The root Tk object of the application.
            graph (Graph): The graph object containing bikeways and park coordinates.
            parks (list): A list of park objects.
            school (School): The school object to be used as a starting point.
        """
        self.root = root
        self.graph = graph
        self.parks = parks
        self.school = school

        self.root.title("Find a Park")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        # Dropdown menu with park names
        self.park_var = tk.StringVar(self.main_frame)
        self.park_var.set("Select a park")
        self.park_dropdown = tk.OptionMenu(self.main_frame, self.park_var, *[park.name for park in self.parks])
        self.park_dropdown.pack()

        # Button to draw the path to the selected park
        self.draw_button = tk.Button(self.main_frame, text="Show path", command=self.draw_path_to_park)
        self.draw_button.pack()

        # Canvas to display the graph
        self.canvas = tk.Canvas(self.main_frame, width=600, height=600)
        self.canvas.pack()

    def draw_path_to_park(self):
        """
        Draw the shortest path to the selected park on the graph and display it on the canvas.
        """
        try:
            # Get the selected park
            selected_park_name = self.park_var.get()
            selected_park = next((park for park in self.parks if park.name == selected_park_name), None)

            if selected_park:
                # Calculate the shortest path to the selected park
                path = self.graph.find_shortest_path(self.graph, self.school, selected_park)

                if path:
                    # Draw the path on the graph
                    img = self.graph.plot_graph(path)

                    # Update the canvas with the new image
                    self.tk_img = ImageTk.PhotoImage(img)
                    self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
                else:
                    print("No path found to the selected park.")
            else:
                print("No park selected.")
        except Exception as e:
            print(f"An error occurred while drawing the path to the park: {e}")

