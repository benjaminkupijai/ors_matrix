"""
Module for schema check tests.
"""

import pandas as pd
from pytest import raises
from pandera.errors import SchemaError
from src.schemas import schemas


def test_input_schema_simple_pass():
    """
    Tests input schema with correct, required columns.
    """
    input_df = pd.DataFrame({
        "id": ["BE", "BR"],
        "latitude": [1.0, 2.0],
        "longitude": [-1, 10]
    })

    schemas.input_file_schema.validate(input_df)
    assert True


def test_input_schema_min_max_coords():
    """
    Tests input schema with coordinates on boundaries
    """

    input_df = pd.DataFrame({
        "id": ["BE", "BR"],
        "latitude": [-90, 90],
        "longitude": [-180, 180]
    })

    schemas.input_file_schema.validate(input_df)
    assert True


def test_input_schema_additional_column_pass():
    """
    Tests input schema with additional non necessary columns
    """

    input_df = pd.DataFrame({
        "id": ["BE", "BR"],
        "address": ["street 1", "street 2"],
        "latitude": [0, 2],
        "longitude": [-30, 30],
        "other_column": ["a", "b"]
    })

    schemas.input_file_schema.validate(input_df)
    assert True


def test_input_schema_unique_id_err():
    """
    Tests for SchemaError when id column has duplicates
    """

    input_df = pd.DataFrame({
        "id": ["BE", "BE"],
        "latitude": [1, 2],
        "longitude": [2, 3]
    })

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "series 'id' contains duplicate values"

    assert expected_err_msg in str(exc.value)


def test_input_schema_latitude_dtype_str_err():
    """
    Tests for SchemaError when latitude is a string
    """

    input_df = pd.DataFrame({
        "id": ["ABN", "ES"],
        "latitude": ["a", 2],
        "longitude": [1, 2]
    })

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "column has non numeric values"

    assert expected_err_msg in str(exc.value)
    assert "'latitude'" in str(exc.value)

def test_input_schema_latitude_dtype_bool_err():
    """
    Tests for SchemaError when latitude is a string
    """

    input_df = pd.DataFrame({
        "id": ["ABN", "ES"],
        "latitude": [True, 2],
        "longitude": [1, 2]
    })

    with raises(SchemaError) as exc:
        schemas.input_file_schema.validate(input_df)

    expected_err_msg = "column has non numeric values"

    assert expected_err_msg in str(exc.value)
    assert "'latitude'" in str(exc.value)


def test_input_schema_latitude_out_of_bound_neg():
    """
    Tests for SchemaError when latitude is smaller than -90
    """

    input_df = pd.DataFrame({
        "id": ["BE", "BR"],
        "latitude": [-90.1, 0],
        "longitude": [0, 1]
    })

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
