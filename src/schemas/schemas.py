"""
Setting schema for data
"""

from typing import Any

import pandera as pa
import pandas as pd
from pandera import DataFrameSchema, Column, Check



def is_numeric(value: Any) -> bool:
    """
    Checks if the given value is either a float or an int.
    """

    return isinstance(value, (int, float)) and not isinstance(value, bool)


def check_is_numeric(s: pd.Series) -> pd.Series:
    """
    Checks if values in series are float or int dtypes. Returns a boolean series.
    """
    return s.map(is_numeric)


numeric_check = pa.Check(
    check_fn=check_is_numeric,
    error="column has non numeric values"
)


input_file_schema = DataFrameSchema(
    {
        "id": Column(pa.String, unique=True),
        "latitude": Column(checks=[numeric_check, Check.le(90), Check.ge(-90)]),
        "longitude": Column(checks=[numeric_check,Check.le(180), Check.ge(-180)])
    },
    strict=False,
    coerce=True
)
