"""
Module for schema check tests.
"""

import pandas as pd
from pytest import raises, fixture
from pandera.errors import SchemaError
from src.schemas import schemas


@fixture(name="input_df")
def input_df_fixture():
    """Returns an input dataframe that passes input_file_schema"""
    df = pd.DataFrame({
        "id": ["BE", "BR"],
        "latitude": [-10, 10],
        "longitude": [-120, 120]
    })

    return df

def test_input_schema_simple_pass(input_df):
    """
    Tests input schema with correct, required columns.
    """
    schemas.input_file_schema.validate(input_df)
    assert True


def test_input_schema_min_max_coords(input_df):
    """
    Tests input schema with coordinates on boundaries
    """

    input_df["longitude"] = [-180, 180]
    input_df["latitude"] = [-90, 90]

    schemas.input_file_schema.validate(input_df)
    assert True


def test_input_schema_additional_column_pass(input_df):
    """
    Tests input schema with additional non necessary columns
    """

    input_df["address"] = ["street 1", "street 2"]
    input_df["other_column"] = ["a", "b"]

    schemas.input_file_schema.validate(input_df)
    assert True

def test_input_schema_missing_id_column(input_df):
    """Tests if SchemaError is raised when id column is missing"""

    input_df.drop(columns="id", inplace=True)

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_error_msg = "column 'id' not in dataframe."

    assert expected_error_msg in str(exc.value)

def test_input_schema_missing_latitude_column(input_df):
    """Tests if SchemaError is raiseed when latitude column in missing"""

    input_df.drop(columns="latitude", inplace=True)

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_error_message = "column 'latitude' not in dataframe."

    assert expected_error_message in str(exc.value)

def test_input_schema_missing_longitude_column(input_df):
    """Tests if SchemaError is raised when longitude column is missing."""

    input_df.drop(columns="longitude", inplace=True)

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_messag = "column 'longitude' not in dataframe."

    assert expected_err_messag in str(exc.value)

def test_input_schema_unique_id_err(input_df):
    """
    Tests for SchemaError when id column has duplicates
    """
    input_df["id"] = ["BE", "BE"]

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "series 'id' contains duplicate values"

    assert expected_err_msg in str(exc.value)


def test_input_schema_latitude_dtype_str_err(input_df):
    """
    Tests for SchemaError when latitude is a string
    """

    input_df["latitude"] = [1, "a"]

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "column has non numeric values"

    assert expected_err_msg in str(exc.value)
    assert "'latitude'" in str(exc.value)

def test_input_schema_latitude_dtype_bool_err(input_df):
    """
    Tests for SchemaError when latitude is a string
    """

    input_df["latitude"] = [True, 2]

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "column has non numeric values"

    assert expected_err_msg in str(exc.value)
    assert "'latitude'" in str(exc.value)


def test_input_schema_latitude_out_of_bound_neg(input_df):
    """
    Tests for SchemaError when latitude is smaller than -90
    """

    input_df["latitude"] = [-90.1, 0]

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "greater_than_or_equal_to(-90)"

    assert expected_err_msg in str(exc.value)
    assert "'latitude'" in str(exc.value)


def test_input_schema_latitude_out_of_bounds_pos():
    """
    Tests for SchemaError when latitude is greater than 90
    """

    input_df = pd.DataFrame({
        "id": ["be", "br"],
        "latitude": [0, 91],
        "longitude": [0, 1]
    })

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "less_than_or_equal_to(90)"

    assert expected_err_msg in str(exc.value)
    assert "'latitude'" in str(exc.value)


def test_input_schema_longitude_out_of_bounds_neg():
    """
    Tests for SchemaError when longitude is less than -180
    """

    input_df = pd.DataFrame({
        "id": ["BE", "BR"],
        "latitude": [9, 10],
        "longitude": [-181, 80]
    })

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "greater_than_or_equal_to(-180)"

    assert expected_err_msg in str(exc.value)
    assert "'longitude'" in str(exc.value)


def test_input_schema_longitude_out_of_bounds_pos():
    """
    Tests for SchemaError when longitude is greater than 180
    """

    input_df = pd.DataFrame({
        "id": ["BE", "BR"],
        "latitude": [0, 1],
        "longitude": [0, 180.001]
    })

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "less_than_or_equal_to(180)"

    assert expected_err_msg in str(exc.value)
    assert "'longitude'" in str(exc.value)
