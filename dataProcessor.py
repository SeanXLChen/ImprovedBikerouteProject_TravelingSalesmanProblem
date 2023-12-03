import requests
import geopandas as gpd

PARKDATA = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/parks-polygon-representation/exports/csv?lang=en&timezone=America%2FLos_Angeles&use_labels=true&delimiter=%3B'
BIKEDATA = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/bikeways/exports/csv?lang=en&timezone=America%2FLos_Angeles&use_labels=true&delimiter=%3B'
VANCOUVERMAP = 'https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/exports/geojson?lang=en&timezone=America%2FLos_Angeles'


def download_csv_file(url):
    """
    Downloads CSV data from a given URL.

    :param url: The URL of the CSV file.
    :return: The raw CSV data as a string, or None if an error occurs.
    :raises: ValueError if the response content type is not CSV.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type')
        if 'csv' not in content_type:
            raise ValueError("The URL does not contain CSV data")

        raw_data = response.text
        return raw_data

    except requests.exceptions.HTTPError as he:
        print(f"HTTP error: {he}")
        return None
    except requests.exceptions.ConnectionError as re:
        print(f"Request error: {re}")
        return None
    except ValueError as ve:
        print(f"Value error: {ve}")
        return None
    except requests.exceptions.Timeout as te:
        print(f"Request error: {te}")
        return None
    

def parse_csv_data(raw_data):
    """
    Parses raw CSV data into a nested list.
    
    :param raw_data: The raw CSV data as a string.
    :return: A list of lists containing the CSV data, or None if an error occurs.
    """
    try:
        lines = raw_data.splitlines()
        data = [line.split(';') for line in lines]
        if len(data) == 0:
            raise ValueError("The CSV data is empty")
        return data
    except ValueError as e:
        print(f"Error with CSV data: {e}")
        return None


def extract_coordinates(geom_str):
    """
    Extracts coordinates from a geometry string.
    
    :param geom_str: A string containing coordinate data.
    :return: A list of (latitude, longitude) pairs.
    """
    start = geom_str.find("[[")
    end = geom_str.find("]]")
    coordinates_string = geom_str[start + 1:end + 1]
    coordinates_list = coordinates_string.split("], [")
    coordinates = []

    for coord_str in coordinates_list:
        lat, lon = coord_str.strip("[]").split(", ")
        lat = float(lat)
        lon = float(lon)
        coordinates.append([lat, lon])

    return coordinates

def extract_index_str(row, substring):
    """
    Finds the index of a substring in a list of strings.
    
    :param row: A list of strings.
    :param substring: The substring to search for.
    :return: The index of the substring.
    """
    index = row.index(substring)
    return index


# Replace the URL with actual dataset URL

# VANVOUCER MAP DATA init
def read_geojson_from_url(url):
    """
    Reads GeoJSON data from the provided URL, and converts it to a GeoDataFrame.

    Args:
        url (str): The URL containing the GeoJSON data.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the data from the GeoJSON.
    """
    response = requests.get(url)
    geojson_data = response.json()
    gdf = gpd.GeoDataFrame.from_features(geojson_data)
    return gdf
    
def data_init():
    """
    init all the dataset above and clean the data
    """

    # Bikeway data init
    dataset_url = BIKEDATA
    raw_data = download_csv_file(dataset_url)
    parsed_data =  parse_csv_data(raw_data)
    index =  extract_index_str(parsed_data[0], "Geom")

    for row in parsed_data[1:]:  # Start from 1 to skip the header row
        row[index] =  extract_coordinates(row[index])


    # Park data init
    parkset_url = PARKDATA
    park_data =  parse_csv_data(download_csv_file(parkset_url))
    park_index =  extract_index_str(park_data[0],"\ufeffGeom")
    parkname_index =  extract_index_str(park_data[0],"PARK_NAME")

    for row in park_data[1:]:
        row[park_index] =  extract_coordinates(row[park_index])
    
    # map boundary init
    boundary_data_gpd = read_geojson_from_url(VANCOUVERMAP)
    return parsed_data, park_data, boundary_data_gpd, index, park_index, parkname_index
