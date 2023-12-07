from classbuilder import *
import unittest
from parkbuilder import *
from startpointbuilder import *

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    def test_add_vertex(self):
        """
        Tests the add_vertex method.
        """
        # happy case
        coordinate = (49.267, -123.12)
        self.graph.add_vertex(coordinate)
        self.assertIn(coordinate, self.graph.vertices)

        # regular
        coordinate1 = (0, 0)
        coordinate2 = (1, 1)
        self.graph.add_vertex(coordinate1)
        self.graph.add_vertex(coordinate2)
        self.assertIn(coordinate1, self.graph.vertices)
        self.assertIn(coordinate2, self.graph.vertices)

    def test_add_edge(self):
        """
        Tests the add_edge method.
        """
        # Error handle case
        with self.assertRaises(ValueError) as e:
            coord = (49.267, -123.12)
            info = 'A'
            distance = 0
            self.assertTrue(self.graph.add_edge(coord,coord,info,info,distance), "Both coordinates must be in the graph before creating an edge." in e.exception)

        # happy case        
        coord1 = (49.267, -123.12)
        coord2 = (49.268, -123.11)
        info1 = 'A'
        info2 = 'B'
        distance = 1
        self.graph.add_vertex(coord1)
        self.graph.add_vertex(coord2)
        self.graph.add_edge(coord1, coord2, info1, info2, distance)
        self.assertIsNotNone(self.graph.vertices[coord1].head)
        self.assertIsNotNone(self.graph.vertices[coord2].head)

    def test_add_edge_bidirectional(self):
        """
        Tests the add_edge method but the case is bidirectional: using it for correctly adding trajectory.
        """
        coord1 = (37.7749, -122.4194)
        coord2 = (37.7849, -122.4294)
        self.graph.add_vertex(coord1)
        self.graph.add_vertex(coord2)
        self.graph.add_edge(coord1, coord2, "info1", "info2", 1.0)
        neighbors1 = self.graph.get_neighbors(coord1)
        neighbors2 = self.graph.get_neighbors(coord2)
        self.assertIn((coord2, "info2", 1.0), neighbors1)
        self.assertIn((coord1, "info1", 1.0), neighbors2)

    def test_haversine_distance(self):
        """
        Tests the haversine_distance method.
        """
        # Regular case
        coord1 = (0, 0)
        coord2 = (0, 0)
        distance = self.graph.haversine_distance(coord1, coord2)
        self.assertEqual(distance, 0)

        # Happy case
        coord1 = (49.267, -123.12)
        coord2 = (49.268, -123.11)
        distance = self.graph.haversine_distance(coord1, coord2)
        self.assertAlmostEqual(distance, 0.734049, delta=0.001)

    def test_find_closest_vertex(self):
        """
        Tests the find_closest_vertex method.
        """
        #regular case
        coord1 = (0, 0)
        coord2 = (1, 1)
        coord3 = (2, 2)
        self.graph.add_vertex(coord1)
        self.graph.add_vertex(coord2)
        closest_vertex, min_distance = self.graph.find_closest_vertex(coord3)
        # coord 2 is more close than 3 to 1
        self.assertEqual(closest_vertex, coord2)
        self.assertAlmostEqual(min_distance, 157.22543203807288, delta=0.001)


        #happy case
        coord1 = (49.267, -123.12)
        coord2 = (49.268, -123.11)
        coord3 = (49.269, -123.10)
        self.graph.add_vertex(coord1)
        self.graph.add_vertex(coord2)
        closest_vertex, min_distance = self.graph.find_closest_vertex(coord3)
        self.assertEqual(closest_vertex, coord2)
        self.assertAlmostEqual(min_distance, 0.734049, delta=0.001)

    def test_get_neighbors(self):
        """
        Tests the get_neighbors method.
        """
        # regular case
        coord1 = (0, 0)
        coord2 = (1, 1)
        coord3 = (2, 2)
        info1 = 'A'
        info2 = 'B'
        info3 = 'C'
        distance1 = 1
        distance2 = 2
        self.graph.add_vertex(coord1)
        self.graph.add_vertex(coord2)
        self.graph.add_vertex(coord3)
        self.graph.add_edge(coord1, coord2, info1, info2, distance1)
        # 1 - 2 connected, for 1, 2 is its near vertex, 3 is not near vertex
        neighbors = self.graph.get_neighbors(coord1)
        self.assertEqual(len(neighbors), 1)
        self.assertIn((coord2, info2, distance1), neighbors)
        self.assertNotIn((coord3, info3, distance2), neighbors)

        # happy case
        coord1 = (49.267, -123.12)
        coord2 = (49.268, -123.11)
        coord3 = (49.269, -123.10)
        info1 = 'A'
        info2 = 'B'
        info3 = 'C'
        distance1 = 1
        distance2 = 2
        self.graph.add_vertex(coord1)
        self.graph.add_vertex(coord2)
        self.graph.add_vertex(coord3)
        # 3- 1 -2 connected graph, for vectex 1, 3 and 2 are it's near vertices
        self.graph.add_edge(coord1, coord2, info1, info2, distance1)
        self.graph.add_edge(coord1, coord3, info1, info3, distance2)
        neighbors = self.graph.get_neighbors(coord1)
        self.assertEqual(len(neighbors), 2)
        self.assertIn((coord2, info2, distance1), neighbors)
        self.assertIn((coord3, info3, distance2), neighbors)

    def test_find_shortest_path(self):
        """
        Tests the get_neighbors method.
        """
        coordinates = [(49.270, -123.11)]
        center_point = (49.2600, -123.2300)
        name1 = "Test Park"

        park = Park(coordinates, center_point, name1)

        name2 = "Test School"
        coordinates = [(49.267, -123.12)]
        startpoint = StartPoint(name2, coordinates)

        coord1 = (49.267, -123.12)
        coord2 = (49.268, -123.11)
        coord3 = (49.269, -123.10)
        coord4 = (49.270, -123.11)
        coord5 = (49.271, -123.11)
        info1 = 'A'
        info2 = 'B'
        distance1 = 1
        distance2 = 2
        distance3 = 1
        distance4 = 1
        distance5 = 1
        self.graph.add_vertex(coord1)
        self.graph.add_vertex(coord2)
        self.graph.add_vertex(coord3)
        self.graph.add_vertex(coord4)
        self.graph.add_vertex(coord5)
        self.graph.add_edge(coord1, coord2, info1, info2, distance1)
        self.graph.add_edge(coord2, coord3, info1, info2, distance2)
        self.graph.add_edge(coord3, coord4, info1, info2, distance3)
        self.graph.add_edge(coord1, coord5, info1, info2, distance4)
        self.graph.add_edge(coord4, coord5, info1, info2, distance5)
        self.graph.add_edge(coord5, coord1, info1, info2, distance5)
        # 1 - 2 - 3 - 4
        # |           |
        # 5 ———————————
        startpoint.cooridinates = coord1
        park.coorindates = coord4
        path = self.graph.find_shortest_path(self.graph, park, startpoint)
        expected_path = [coord4, coord5, coord1]
        self.assertEqual(path, expected_path)

if __name__ == '__main__':
    unittest.main()