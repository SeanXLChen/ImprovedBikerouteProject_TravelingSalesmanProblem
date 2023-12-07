import unittest
from startpointbuilder import StartPoint

class TestStartPoint(unittest.TestCase):
    """
    A unittest class for testing the StartPoint class.
    """

    def test_init(self):
        """
        Test the __init__ method of the StartPoint class for various cases.
        """

        # Regular case
        name = "Test School"
        coordinates = [(49.2609, -123.2460)]
        school = StartPoint(name, coordinates)
        self.assertEqual(school.name, name)
        self.assertEqual(school.coordinates, coordinates)

        # Empty name
        name = ""
        school = StartPoint(name, coordinates)
        self.assertEqual(school.name, name)

        # Missing coordinates
        coordinates = []
        school = StartPoint(name, coordinates)
        self.assertEqual(school.coordinates, coordinates)

if __name__ == '__main__':
    unittest.main()