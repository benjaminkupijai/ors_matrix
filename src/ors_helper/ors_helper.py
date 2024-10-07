"""
This module sends requests to the openrouteservice server and generates
and generates the final output
"""
from typing import Union
import openrouteservice as ors

class ORShelper:
    """
    Class to handle the requests to the OpenRouteService server. And transform
    the data.
    """
    def __init__(self, server_url: str, api_key: Union[str, None]=None):
        self.client = ors.Client(base_url=server_url, key=api_key)
