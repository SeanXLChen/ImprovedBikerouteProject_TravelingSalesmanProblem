import unittest
from dataProcessor import *

VANCOUVERMAP = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/exports/geojson?lang=en&timezone=America%2FLos_Angeles'
WRONGDATAURL = "http://none_exist.com/data.csv"


class TestDataProcessor(unittest.TestCase):

    def test_successful_download(self):
        """Test case for a successful download of CSV data from a URL.
        
        This test case checks if the downloaded data has a 200 status code, indicating a successful download.
        """
        url = VANCOUVERMAP
        status_code = 200
        raw_data = requests.get(url)
        self.assertEqual(status_code, raw_data.status_code)

    def test_http_error(self):
        """Test case for an HTTP error when downloading CSV data from a URL.
        
        This test case checks if the download_csv_file function returns None when encountering an HTTP error.
        """
        response = requests.Response()
        response.status_code = 404
        response.raise_for_status = lambda: response.raise_exception()
        url = WRONGDATAURL
        result = download_csv_file(url)
        self.assertIsNone(result)

    def test_content_type_error(self):
        """Test case for a content type error when downloading CSV data from a URL.
        
        This test case checks if the download_csv_file function returns None when the content type is not CSV.
        """
        url = WRONGDATAURL
        result = download_csv_file(url)
        self.assertIsNone(result)
    
    def test_parse_csv_data(self):
        """Test case for parsing CSV data from a raw string.
        
        This test case checks if the parse_csv_data function correctly processes the raw string and returns the expected data structure.
        """
        raw_data = "a;b;c\n1;2;3\n4;5;6"
        expected_data = [["a", "b", "c"], ["1", "2", "3"], ["4", "5", "6"]]
        parsed_data = parse_csv_data(raw_data)
        self.assertEqual(parsed_data, expected_data)

    def test_extract_coordinates(self):
        """Test case for extracting coordinates from a geometry string.
        
        This test case checks if the extract_coordinates function correctly processes the geometry string and returns the expected coordinates.
        """
        geom_str = "POINT ([[123.456, -78.901]])"
        expected_coordinates = [[123.456, -78.901]]
        coordinates = extract_coordinates(geom_str)
        self.assertEqual(coordinates, expected_coordinates)

    def test_extract_index_str(self):
        """Test case for extracting an index from a list based on a substring.
        
        This test case checks if the extract_index_str function correctly finds the index of an element containing the specified substring in the given list.
        """
        row = ["a", "b", "c"]
        substring = "b"
        expected_index = 1
        index = extract_index_str(row, substring)
        self.assertEqual(index, expected_index)


if __name__ == "__main__":
    unittest.main()