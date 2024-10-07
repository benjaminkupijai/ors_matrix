"""Tests for the ORShelper class"""

import openrouteservice as ors
from src.ors_helper import ors_helper


def test_ors_helper_init():
    """Tests if ORShelper gets correctly initialized"""

    test_instance = ors_helper.ORShelper(
        server_url="http://127.0.0.1")

    assert isinstance(test_instance, ors_helper.ORShelper)
    assert isinstance(test_instance.client, ors.Client)
