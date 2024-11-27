"""
Unit tests for ors_utils.py
"""
from src.ors_helper import ors_utils

def test_chunks_list():
    """Tests the chunks generator that yields n-sized chunks of a list"""

    iterator_list = [1, 2, 3, 4, 5]
    result_list = []

    for chunk in ors_utils.chunks(to_iterate=iterator_list, chunk_size=2):
        result_list += chunk

    assert result_list == iterator_list

def test_chunks_tuple():
    """Tests the chunks generator that yields n-sized chunks of a list"""

    iterator_tuple = (1, 2, 3, 4, 5)
    result_list = []

    for chunk in ors_utils.chunks(to_iterate=iterator_tuple, chunk_size=2):
        result_list += chunk

    assert result_list == list(iterator_tuple)
