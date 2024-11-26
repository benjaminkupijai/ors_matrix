"""
This module sends requests to the openrouteservice server and generates
and generates the final output
"""
import os
from typing import Union, Optional
from dotenv import load_dotenv
import openrouteservice as ors
import pandas as pd
from .ors_utils import chunks

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

    def get_distance_matrix(
            self,
            locations: pd.DataFrame,
            profile: str,
            chunk_size: int=25) -> pd.DataFrame:
        """
        Generates a distance matrix from a locations list. With the given profile
        'car' or 'hgv'.
        """

        distance_matrix = pd.DataFrame()
        locations_copy = locations.copy()

        if profile not in ['car', 'hgv']:
            raise ValueError(
                "Chosen profile is expected to be 'car' or 'hgv', got {profile}")

        locations_copy["coordinates"] = list( zip(locations["longitude", "latitude"]) )

        for start in chunks(locations_copy, chunk_size=chunk_size):
            for destination in chunks(locations_copy, chunk_size=chunk_size):

                start_list = start["coordinates"].to_list()
                destination_list = destination["coordinates"].to_list()

                range_start = list( range( len(start) ) )

                range_destination = list( range(
                    len(range_start), len(range_start) + len(destination)
                ))

                routes = self.client.distance_matrix(
                    start_list + destination_list,
                    sources=range_start,
                    destination=range_destination,
                    metrics=["duration", "distance"],
                    profile=f"driving-{profile}"
                )

                distance_df = pd.DataFrame(
                    index=start.index,
                    columns=destination.index,
                    data=routes["distances"]
                )
                distance_df.reset_index(names="start_index", inplace=True)
                chunk_distance = distance_df.melt(
                    id_vars="start_index",
                    value_vars=destination.index,
                    var_name="destination_index",
                    value_name="distance"
                )

                duration_df = pd.DataFrame(
                    index=start.index,
                    columns=destination.index,
                    data=routes["durations"]
                )
                duration_df.reset_index(names="start_index", inplace=True)
                chunk_duration = distance_df.melt(
                    id_vars="start_index",
                    value_vars=destination.index,
                    var_name="destination_index",
                    value_name="duration"
                )

                chunk_result = pd.merge(
                    chunk_distance,
                    chunk_duration,
                    on=["start_index", "destination_index"]
                )

            distance_matrix = pd.concat(
                (distance_matrix, chunk_result),
                ignore_index=True
            )

        distance_matrix = pd.merge(
            distance_matrix,
            locations["id"],
            left_on="start_index",
            right_index=True
        ).rename(columns={"id": "start_id"})

        distance_matrix = pd.merge(
            distance_matrix,
            locations["id"],
            left_on="destination_index",
            right_index=True
        ).rename(columns={"id": "destination_id"})

        return distance_matrix
