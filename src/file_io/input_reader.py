"""This module handles file reading and file writing."""

import pandas as pd
from src.schemas.schemas import input_file_schema


def read_xlsx_input_file(path: str) -> pd.DataFrame:
    """Reads xlsx file from device checks input schema and returns dataframe

    Parameter
    ---------
    path : str
        Path to xlsx file. Required columns are 'id', 'longitude' and
        'latitude'.
            - id column can be string, int or float and has to be unique
            - latititude has to be in in the interval [-90, 90]
            - longitude has to be in the interval [-180, 180]
        Additional columns are allowed.

    Returns
    -------
    pd.DataFrame
        DataFrame that passed input_file_schema

    Raises
    ------
    SchemaError
        When the dataframe does not pass the input_file_schema
    """

    input_file_df = pd.read_excel(path)
    input_file_schema.validate(input_file_df)

    return input_file_df
