"""
This module sends requests to the openrouteservice server and generates
and generates the final output
"""
import os
from typing import Union, Optional
from dotenv import load_dotenv
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

    @classmethod
    def from_env_file(cls, dotenv_path: Optional[str] = None) -> 'ORShelper':
        """returns an instance of ORShelper with base_url and API key from .env
        file"""

        load_dotenv(dotenv_path=dotenv_path)
        server_url = os.getenv("SERVER_URL")
        api_key = os.getenv("ORS_API_KEY")

        if server_url is None:
            raise ValueError("No server URL found. Check .env file")

        return ORShelper(server_url=server_url, api_key=api_key)
