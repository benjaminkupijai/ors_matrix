"""Tests for the ORShelper class"""

import openrouteservice as ors
import responses
from src.ors_helper import ors_helper


def test_ors_helper_init():
    """Tests if ORShelper gets correctly initialized"""
    test_url = "http://127.0.0.1"

    test_instance = ors_helper.ORShelper(
        server_url=test_url)

    assert isinstance(test_instance, ors_helper.ORShelper)
    assert isinstance(test_instance.client, ors.Client)
    assert test_instance.server_url == test_url

@responses.activate
def test_ors_helper_check_server_status_200():
    """Checks if a request is made when server status gets checked"""
    url = "http://some-ip"

    responses.add(
        method=responses.GET,
        url=f"{url}/ors/health",
        json={"key": "value"},
        status=200
    )

    helper = ors_helper.ORShelper(server_url=url)

    helper.check_server_status()

    assert helper.server_status == 200
