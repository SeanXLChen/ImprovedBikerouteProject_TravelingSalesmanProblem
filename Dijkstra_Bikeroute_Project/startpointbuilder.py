class StartPoint:
    """A class to represent a school with its name and coordinates."""

    def __init__(self, name, coordinates):
        """
        Initialize a School object.

        Args:
            name (str): The name of the school.
            coordinates (list): A list of coordinates representing the school's location.
        """
        self.name = name
        self.coordinates = coordinates