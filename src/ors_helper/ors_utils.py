"""
Helper functions for ors_helper
"""
from typing import List, Tuple, Union

def chunks(to_iterate: Union[List, Tuple], chunk_size: int):
    """
    A generator function that yields a chunks of 'chunk_size' from a list or
    tuple.
    """

    for i in range(0, len(to_iterate), chunk_size):
        yield to_iterate[i:i+chunk_size]
