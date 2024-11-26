"""Tests for the ORShelper class"""
import os
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

def test_ors_helper_init_from_env_file(tmp_path, monkeypatch):
    """Tests if ors helper is correctly created from .env file"""
    monkeypatch.delenv("SERVER_URL", raising=False)
    monkeypatch.delenv("ORS_API_KEY", raising=False)

    file_name = '.env'

    env_path = os.path.join(tmp_path, file_name)

    test_url = "https://api.testurl.com"
    test_key = "abcdefg"

    content = (
        f"SERVER_URL={test_url}\nORS_API_KEY={test_key}"
    )

    with open(env_path, 'w', encoding='utf-8') as file:
        file.write(content)

    helper = ors_helper.ORShelper.from_env_file(dotenv_path=env_path)

    assert helper.client._key == test_key
    assert helper.client._base_url == test_url
