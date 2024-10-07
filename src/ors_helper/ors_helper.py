"""
This module sends requests to the openrouteservice server and generates
and generates the final output
"""
from typing import Union
import requests
import openrouteservice as ors

class ORShelper:
    """
    Class to handle the requests to the OpenRouteService server. And transform
    the data.
    """
    def __init__(self, server_url: str, api_key: Union[str, None]=None):
        self.server_url=server_url
        self.client = ors.Client(base_url=server_url, key=api_key)
        self.server_status = -1


    def check_server_status(self) -> None:
        """Sends health request to ORS server and sets server status to response.status_code"""

        response = requests.get(f"{self.server_url}/ors/health")

        self.server_status = response.status_code
