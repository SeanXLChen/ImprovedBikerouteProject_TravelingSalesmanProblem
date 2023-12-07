class Park:
    """A class to represent a park with its coordinates, center point, and name."""

    def __init__(self, coordinates, center_point, name):
        """
        Initialize a Park object.

        Args:
            coordinates (list): A list of coordinates representing the park's boundaries.
            center_point (tuple): A tuple (latitude, longitude) representing the park's center point.
            name (str): The name of the park.
        """
        self.coordinates = coordinates
        self.center_point = center_point
        self.name = name

