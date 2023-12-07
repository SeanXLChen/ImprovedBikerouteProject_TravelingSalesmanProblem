'''
CS5001
2023 Spring
Milestone 2 
Yu Ji
'''
import dataProcessor
import classbuilder
import parkbuilder
import guibuilder_geopandas
import startpointbuilder

NEU_COORIDINATES = [(-123.115540, 49.280747)]
SCHOOL_NAME = 'NEU'

def main():
    """
    This script combines all the components (dataProcessor, classbuilder, parkbuilder, and guibuilder) to build a complete
    application that loads and processes bike route and park data, builds a graph, finds the shortest path between a school
    and a park, and provides a graphical user interface (GUI) for user interaction.
    """

# Classes: Node, DoublyLinkedList, Graph, Park, App
# ... (copy all class definitions from the previous answers)

# Functions: build_parks_list
# ... (copy the build_parks_list function from the previous answers)
    parsed_data, park_data, boundary_data_gpd, index, park_index, parkname_index = dataProcessor.data_init()

    # Load and process the data
    graph = classbuilder.Graph()

    try:
        graph.build_graph(parsed_data, index)

    except Exception as e:
        print(f"Error building graph: {e}")

    # Load park data and create Park objects
    Parks = []
    for park_row in park_data[1:]:
        try:
            park_instance = parkbuilder.Park(park_row[park_index], park_row[parkname_index + 2], park_row[parkname_index])
            Parks.append(park_instance)
        except Exception as e:
            print(f"Error creating Park instance: {e}")

    # Load startpoint data and create school objects
        school = startpointbuilder.StartPoint(SCHOOL_NAME, NEU_COORIDINATES)

    # Set up the GUI and run the app
    try:
        root = guibuilder_geopandas.tk.Tk()
        app = guibuilder_geopandas.App(root, graph, Parks, school, boundary_data_gpd)
        root.mainloop()
    except Exception as e:
        print(f"Error running the app: {e}")

    # path = graph.find_shortest_path(graph, school, Parks[0])
    # graph.plot_graph(path)


if __name__ == '__main__':
    main()


