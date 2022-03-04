import json
import requests


class DataFetcher:
    """A class to fetch data from a public API and return a readable JSON file."""

    def __init__(self, data_url, file_name):
        """
        Initialize the attributes of the data fetcher.
        Takes the URL parameter and writes it to a readable JSON format in the filename parameter.
        """
        self.url = data_url
        self.filename = file_name

    def make_api_call(self):
        """Make an API call with the URL. Returns a 'request' object."""
        request_object = requests.get(self.url)
        return request_object

    def convert_to_json(self, request_object):
        """Convert the request object to readable JSON with filename given in class constructor."""
        requested_data = request_object.json()
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(requested_data, f, indent=4)
        return requested_data

