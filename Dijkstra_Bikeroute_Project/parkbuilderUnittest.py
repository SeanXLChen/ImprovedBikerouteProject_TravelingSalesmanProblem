import unittest
from parkbuilder import Park


class TestPark(unittest.TestCase):
    """
    A unittest class for testing the Park class.
    """

    def test_init(self):
        """
        Test the __init__ method of the Park class for various cases.
        """

        # Regular case
        coordinates = [(49.2609, -123.2460), (49.2700, -123.2340), (49.2500, -123.2200)]
        center_point = (49.2600, -123.2300)
        name = "Test Park"

        park = Park(coordinates, center_point, name)
        self.assertEqual(park.coordinates, coordinates)
        self.assertEqual(park.center_point, center_point)
        self.assertEqual(park.name, name)

        # Empty name
        name = ""
        park = Park(coordinates, center_point, name)
        self.assertEqual(park.name, name)

        # Missing coordinates
        coordinates = []
        park = Park(coordinates, center_point, name)
        self.assertEqual(park.coordinates, coordinates)

        # Missing center point
        center_point = None
        park = Park(coordinates, center_point, name)
        self.assertEqual(park.center_point, center_point)

if __name__ == '__main__':
    unittest.main()
