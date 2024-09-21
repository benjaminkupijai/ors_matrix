"""Tests the src.io.file_handler.py module"""
import os

import pandas as pd
from pytest import fixture, raises
from pandera.errors import SchemaError

from src.file_io import input_reader


@fixture(name="input_df")
def input_df_fixture():
    """Returns a input schema conform dataframe for the input file"""
    input_df = pd.DataFrame({
        "id": ["BE", "BE2"],
        "longitude": [-45, 45],
        "latitude": [-30, 30]
    })

    return input_df

def test_read_xlsx_input_file(tmp_path, input_df):
    """Tests if method loads xlsx file properly."""
    path = os.path.join(tmp_path, "temp.xlsx")

    input_df.to_excel(path, index=False)

    result = input_reader.read_xlsx_input_file(path)

    assert result.shape == (2,3)


def test_read_xlsx_input_file_schema_fail(tmp_path, input_df):
    """Tests if SchemaError is raised """
    path = os.path.join(tmp_path, "temp.xlsx")

    input_df.drop(columns="id", inplace=True)

    input_df.to_excel(path, index=False)

    with raises(SchemaError) as exc:
        input_reader.read_xlsx_input_file(path)

    assert isinstance(exc.value, SchemaError)
